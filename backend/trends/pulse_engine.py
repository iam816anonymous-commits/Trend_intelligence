import numpy as np
from sklearn.cluster import AgglomerativeClustering
from backend.embeddings.vector_store import VectorStore
from backend.storage.models import Signal, Topic
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

        if len(signals) < 5: # Minimum threshold for meaningful clustering
            return []

        embeddings = [self.vs.model.encode(s.title + " " + (s.body or "")) for s in signals]
        clustering = AgglomerativeClustering(n_clusters=None, distance_threshold=0.4, metric='cosine', linkage='average')
        labels = clustering.fit_predict(embeddings)

        clusters = {}
        for idx, label in enumerate(labels):
            if label not in clusters:
                clusters[label] = []
            clusters[label].append(signals[idx])

        return clusters

    def generate_topic_name(self, signals):
        # Extract common keywords for better naming
        text = " ".join([s.title for s in signals]).lower()
        words = re.findall(r'\w+', text)
        stopwords = {'the', 'and', 'for', 'with', 'india', 'news', 'recent', 'spike', 'rise'}
        filtered = [w for w in words if len(w) > 3 and w not in stopwords]
        common = Counter(filtered).most_common(3)
        return " ".join([w[0] for w in common]).title()

    def calculate_trend_score(self, cluster):
        # Improved scoring logic
        velocity = len(cluster) / 12.0 # Last 12h normalized
        sources = len(set([s.source for s in cluster]))
        source_diversity = sources / 5.0 # Max diversity score normalized to 5 sources
        regions = len(set([s.region for s in cluster]))

        score = (velocity * 0.4) + (source_diversity * 0.4) + (regions * 0.2)
        return min(score * 100, 100)

    def run(self):
        clusters = self.cluster_signals()
        topics = []
        for signals in clusters.values():
            if len(signals) < 3: continue # Noise reduction

            score = self.calculate_trend_score(signals)
            name = self.generate_topic_name(signals)

            # Check for existing similar topic
            existing = self.db.query(Topic).filter(Topic.name == name).first()
            if existing:
                existing.trend_score = score
                existing.last_updated = datetime.datetime.utcnow()
                topic = existing
            else:
                topic = Topic(
                    name=name,
                    trend_score=score,
                    status="Early" if score < 40 else "Growing" if score < 70 else "Hot",
                    confidence=min(len(signals) * 0.1, 1.0)
                )
                self.db.add(topic)
                self.db.flush() # Get ID

            for s in signals:
                s.topic_id = topic.id

            topics.append(topic)

        self.db.commit()
        return topics
