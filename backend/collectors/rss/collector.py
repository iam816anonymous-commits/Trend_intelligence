import feedparser
import datetime
import logging
from sqlalchemy.orm import Session
from backend.storage.models import Article, Source

logger = logging.getLogger(__name__)

class RSSCollector:
    def collect(self, db: Session, source: Source):
        logger.info(f"Collecting RSS from {source.url}")
        feed = feedparser.parse(source.url)

        for entry in feed.entries:
            # Check if article already exists
            existing = db.query(Article).filter(Article.url == entry.link).first()
            if existing:
                continue

            article = Article(
                title=entry.get("title", ""),
                body=entry.get("summary", "") or entry.get("description", ""),
                source_name=source.name,
                url=entry.link,
                timestamp=datetime.datetime.utcnow(),
                category=source.category,
                country=source.country,
                language=source.language,
                raw_data=dict(entry)
            )
            db.add(article)

        db.commit()
