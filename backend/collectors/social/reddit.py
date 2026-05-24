import requests
import datetime
from sqlalchemy.orm import Session
from backend.storage.models import Signal

class RedditIndiaCollector:
    def collect(self, db: Session):
        # In a real app, use PRAW. For now, we mock the logic.
        print("Collecting from Reddit India...")
        mock_signals = [
            {
                "title": "Heatwave in Indore - cooling towels sold out",
                "body": "Can't find cooling towels anywhere in Indore. Zepto says out of stock.",
                "source": "reddit",
                "url": "https://reddit.com/r/indore/123",
                "category": "Consumer",
                "region": "Indore",
                "type": "consumer"
            },
            {
                "title": "Blinkit movement: Electrolyte drinks spike",
                "body": "Massive orders for electrolyte sachets in Mumbai.",
                "source": "blinkit",
                "url": "https://blinkit.com/trends/1",
                "category": "Consumer",
                "region": "Mumbai",
                "type": "consumer"
            }
        ]

        for s_data in mock_signals:
            existing = db.query(Signal).filter(Signal.url == s_data["url"]).first()
            if not existing:
                signal = Signal(**s_data)
                db.add(signal)

        db.commit()
