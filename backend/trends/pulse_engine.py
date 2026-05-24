import numpy as np
from sklearn.cluster import AgglomerativeClustering
from backend.embeddings.vector_store import VectorStore
from backend.storage.models import Signal, Topic, TopicHistory
import datetime
from collections import Counter
import re

class TrendPulseEngine:
    def __init__(self, db):
        self.db = db
        self.vs = VectorStore()

    def cluster_signals(self, hours=24):
        since = datetime.datetime.utcnow() - datetime.timedelta(hours=hours)
        signals = self.db.query(Signal).filter(Signal.timestamp >= since, Signal.topic_id == None).all()

        if len(signals) < 3:
            return {}

        embeddings = [self.vs.model.encode(s.title + " " + (s.body or "")) for s in signals]
        clustering = AgglomerativeClustering(n_clusters=None, distance_threshold=0.35, metric='cosine', linkage='average')
        labels = clustering.fit_predict(embeddings)

        clusters = {}
        for idx, label in enumerate(labels):
            if label not in clusters: clusters[label] = []
            clusters[label].append(signals[idx])

        return clusters

    def generate_topic_summary(self, signals):
        # Improved naming logic using highest impact signal title or keyword extraction
        # For simplicity, we use the title of the most impactful signal
        best_signal = max(signals, key=lambda s: s.impact_score if s.impact_score else 0)
        return best_signal.title[:100]

    def calculate_trend_score(self, cluster):
        # score = velocity * .3 + growth * .25 + geo_spread * .2 + source_diversity * .25
        velocity = len(cluster) / 12.0
        now = datetime.datetime.utcnow()
        recent = len([s for s in cluster if s.timestamp >= now - datetime.timedelta(hours=6)])
        older = len(cluster) - recent
        growth = (recent - older) / (older + 1)

        regions = len(set([s.region for s in cluster]))
        sources = len(set([s.source for s in cluster]))

        score = (velocity * 0.3) + (growth * 0.25) + (regions / 10.0 * 0.2) + (sources / 5.0 * 0.25)
        return min(score * 100, 100)

    def find_similar_topic(self, text):
        # Use semantic search to find an existing topic that matches this cluster
        results = self.vs.search(text, limit=1)
        if results and results[0].score > 0.85:
            topic_id = results[0].payload.get("topic_id")
            if topic_id:
                return self.db.query(Topic).get(topic_id)
        return None

    def run(self):
        clusters = self.cluster_signals()
        topics = []
        for signals in clusters.values():
            if len(signals) < 3: continue

            cluster_text = " ".join([s.title for s in signals[:5]])
            score = self.calculate_trend_score(signals)

            # Check for existing topic via semantic search
            topic = self.find_similar_topic(cluster_text)

            if not topic:
                name = self.generate_topic_summary(signals)
                topic = Topic(
                    name=name,
                    trend_score=score,
                    status="Early",
                    confidence=min(len(signals) * 0.1, 1.0)
                )
                self.db.add(topic)
                self.db.flush()
                # Store in vector DB for future matching
                self.vs.upsert_article(f"topic_{topic.id}", name, {"topic_id": topic.id, "type": "topic"})
            else:
                topic.trend_score = score
                topic.last_updated = datetime.datetime.utcnow()

            # Record history
            history = TopicHistory(topic_id=topic.id, score=score)
            self.db.add(history)

            for s in signals:
                s.topic_id = topic.id

            topics.append(topic)

        self.db.commit()
        return topics
