from sqlalchemy.orm import Session
from backend.storage.models import TopicHistory
import datetime
import numpy as np

class PredictionEngine:
    def calculate_momentum(self, topic_id: int, db: Session):
        # Fetch last 5 snapshots
        history = db.query(TopicHistory).filter(TopicHistory.topic_id == topic_id).order_by(TopicHistory.timestamp.desc()).limit(5).all()

        if len(history) < 2:
            return 0.0

        scores = [h.score for h in reversed(history)]
        # Simple slope calculation
        x = np.arange(len(scores))
        y = np.array(scores)
        slope, _ = np.polyfit(x, y, 1)

        return float(slope)

    def viral_probability(self, momentum: float, confidence: float):
        # Heuristic for virality
        prob = (momentum * 0.7) + (confidence * 0.3)
        return min(max(prob, 0.0), 1.0)
