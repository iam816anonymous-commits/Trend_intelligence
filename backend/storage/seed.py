from backend.storage.models import SessionLocal, Source

def seed_sources():
    db = SessionLocal()
    sources = [
        {"name": "The Hindu", "url": "https://www.thehindu.com/news/national/feeder/default.rss", "type": "rss", "category": "Politics"},
        {"name": "Times of India", "url": "https://timesofindia.indiatimes.com/rssfeeds/296589292.cms", "type": "rss", "category": "World"},
        {"name": "NDTV News", "url": "https://feeds.feedburner.com/ndtvnews-top-stories", "type": "rss", "category": "General"},
        {"name": "YourStory", "url": "https://yourstory.com/feed", "type": "rss", "category": "Startup"},
        {"name": "Economic Times", "url": "https://economictimes.indiatimes.com/rssfeedstopstories.cms", "type": "rss", "category": "Business"},
        {"name": "Livemint", "url": "https://www.livemint.com/rss/news", "type": "rss", "category": "Finance"},
        {"name": "India Today", "url": "https://www.indiatoday.in/rss/1206578", "type": "rss", "category": "General"},
    ]

    for s_data in sources:
        existing = db.query(Source).filter(Source.url == s_data["url"]).first()
        if not existing:
            source = Source(**s_data)
            db.add(source)

    db.commit()
    db.close()

if __name__ == "__main__":
    seed_sources()
