import logging
from backend.storage.models import SessionLocal
from backend.collectors.rss.collector import RSSCollector
from backend.trends.pulse_engine import TrendPulseEngine
from backend.trends.opportunity import OpportunityFinder

logger = logging.getLogger("TaskManager")

class TaskManager:
    def __init__(self):
        self.db = SessionLocal()

    def run_collection_task(self):
        logger.info("Task: Running collection...")
        # RSS is just one type. In a full system we'd loop through all collectors.
        sources = [
            {"name": "The Hindu", "url": "https://www.thehindu.com/news/national/feeder/default.rss", "category": "Politics"},
            {"name": "YourStory", "url": "https://yourstory.com/feed", "category": "Startup"}
        ]
        for s in sources:
            collector = RSSCollector(s['name'], s['url'], s['category'])
            collector.collect(self.db)
        logger.info("Task: Collection complete.")

    def run_clustering_task(self):
        logger.info("Task: Running clustering...")
        engine = TrendPulseEngine(self.db)
        topics = engine.run()
        logger.info(f"Task: Clustering complete. {len(topics)} topics updated.")

    def run_opportunity_task(self):
        logger.info("Task: Running opportunity discovery...")
        finder = OpportunityFinder(self.db)
        opps = finder.find_opportunities()
        logger.info(f"Task: Discovery complete. {len(opps)} new opportunities found.")

    def close(self):
        self.db.close()
