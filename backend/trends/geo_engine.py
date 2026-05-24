from sqlalchemy.orm import Session
from backend.storage.models import Signal
from collections import Counter
import numpy as np

class GeoEngine:
    def __init__(self, db: Session):
        self.db = db

    def get_regional_hotspots(self):
        signals = self.db.query(Signal).all()
        if not signals: return {}

        counts = Counter([s.region for s in signals])
        mean_val = np.mean(list(counts.values()))
        std_val = np.std(list(counts.values())) if len(counts) > 1 else 1.0

        hotspots = {}
        for city, count in counts.items():
            # Z-score based hotspot detection
            z_score = (count - mean_val) / std_val

            city_signals = [s for s in signals if s.region == city]
            top_topics = Counter([s.topic.name for s in city_signals if s.topic]).most_common(2)

            hotspots[city] = {
                "signal_count": count,
                "z_score": float(z_score),
                "hotness": "High" if z_score > 1.5 else "Medium" if z_score > 0 else "Normal",
                "top_drivers": [t[0] for t in top_topics]
            }

        return hotspots
