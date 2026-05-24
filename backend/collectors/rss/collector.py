from backend.collectors.base import BaseCollector
from sqlalchemy.orm import Session
import feedparser
import datetime

class RSSCollector(BaseCollector):
    def __init__(self, source_name, url, category):
        self.source_name = source_name
        self.url = url
        self.category = category

    def collect(self, db: Session):
        feed = feedparser.parse(self.url)
        signals = []
        for entry in feed.entries:
            signals.append({
                "title": entry.get("title", ""),
                "body": entry.get("summary", "") or entry.get("description", ""),
                "source": self.source_name,
                "url": entry.link,
                "timestamp": datetime.datetime.utcnow(),
                "category": self.category,
                "type": "news"
            })
        return self.save_signals(db, signals)
