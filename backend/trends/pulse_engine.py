import numpy as np
from sklearn.cluster import AgglomerativeClustering
from backend.embeddings.vector_store import VectorStore
from backend.storage.models import Signal, Topic
import datetime

class TrendPulseEngine:
    def __init__(self, db):
        self.db = db
        self.vs = VectorStore()

    def cluster_signals(self, hours=24):
        since = datetime.datetime.utcnow() - datetime.timedelta(hours=hours)
        signals = self.db.query(Signal).filter(Signal.timestamp >= since).all()

        if len(signals) < 2:
            return []

        # 1. Get embeddings
        embeddings = [self.vs.model.encode(s.title + " " + s.body) for s in signals]

        # 2. Perform clustering
        clustering = AgglomerativeClustering(n_clusters=None, distance_threshold=0.5, metric='cosine', linkage='average')
        labels = clustering.fit_predict(embeddings)

        clusters = {}
        for idx, label in enumerate(labels):
            if label not in clusters:
                clusters[label] = []
            clusters[label].append(signals[idx])

        return clusters

    def calculate_trend_score(self, cluster):
        # trend_score = (velocity * .3 + source_growth * .25 + geo_spread * .15 + commerce_signal * .2 + social_acceleration * .1)
        velocity = len(cluster) / 24.0 # simple velocity
        source_growth = 1.5 # placeholder
        geo_spread = len(set([s.region for s in cluster])) / 10.0
        commerce_signal = 1.0 if any(s.source in ['blinkit', 'zepto', 'amazon'] for s in cluster) else 0.5
        social_acceleration = 1.2 # placeholder

        score = (
            velocity * 0.3 +
            source_growth * 0.25 +
            geo_spread * 0.15 +
            commerce_signal * 0.2 +
            social_acceleration * 0.1
        )
        return min(score * 100, 100)

    def update_topics(self):
        clusters = self.cluster_signals()
        topics = []
        for label, signals in clusters.items():
            score = self.calculate_trend_score(signals)
            name = signals[0].title[:50] # heuristic for name

            status = "Early"
            if score > 80: status = "Peak"
            elif score > 60: status = "Hot"
            elif score > 40: status = "Growing"

            topic = Topic(
                name=name,
                trend_score=score,
                status=status,
                last_updated=datetime.datetime.utcnow()
            )
            topics.append(topic)

        return topics
