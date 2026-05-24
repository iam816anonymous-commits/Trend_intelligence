from sqlalchemy.orm import Session
from backend.storage.models import Article
import datetime
from collections import Counter

class TrendDetector:
    def detect_trends(self, db: Session, hours: int = 24):
        since = datetime.datetime.utcnow() - datetime.timedelta(hours=hours)
        articles = db.query(Article).filter(Article.timestamp >= since).all()

        # Simple keyword-based trend detection for Phase 4
        # In later phases, we'll use clustering on embeddings
        words = []
        for article in articles:
            words.extend(article.title.lower().split())

        common_words = Counter(words).most_common(20)

        trends = []
        for word, count in common_words:
            if len(word) > 4: # Ignore small words
                trends.append({
                    "trend": word,
                    "count": count,
                    "growth": "+50%", # Placeholder
                    "strength": min(count * 10, 100)
                })

        return sorted(trends, key=lambda x: x['strength'], reverse=True)
