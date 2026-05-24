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
        from backend.storage.models import Signal
        sources = db.query(Signal.source).filter(
            Signal.title.contains(trend_name)
        ).distinct().count()

        return min(sources * 10, 100)

    def forecast_30_day_probability(self, trend_name, db: Session):
        # 30-day forecast heuristic
        return 0.75 # placeholder 75% probability
