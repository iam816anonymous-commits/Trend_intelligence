from sqlalchemy.orm import Session
from backend.storage.models import Article
import datetime

class PredictionEngine:
    def predict_momentum(self, trend_name, db: Session):
        # In a real system, this would use time-series analysis
        # For now, we use a simple heuristic based on recent mentions
        count_last_3h = db.query(Article).filter(
            Article.title.contains(trend_name),
            Article.timestamp >= datetime.datetime.utcnow() - datetime.timedelta(hours=3)
        ).count()

        count_last_12h = db.query(Article).filter(
            Article.title.contains(trend_name),
            Article.timestamp >= datetime.datetime.utcnow() - datetime.timedelta(hours=12)
        ).count()

        if count_last_3h > (count_last_12h / 4):
            return "Rising"
        return "Stable"

    def viral_probability(self, trend_name, db: Session):
        # Heuristic: multi-source coverage increases virality
        sources = db.query(Article.source_name).filter(
            Article.title.contains(trend_name)
        ).distinct().count()

        return min(sources * 10, 100)
