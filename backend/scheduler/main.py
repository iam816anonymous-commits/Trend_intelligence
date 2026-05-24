import time
import logging
from backend.storage.models import SessionLocal, Source
from backend.collectors.rss.collector import RSSCollector

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("scheduler")

def run_scheduler():
    rss_collector = RSSCollector()
    while True:
        logger.info("Starting collection cycle...")
        db = SessionLocal()
        try:
            sources = db.query(Source).filter(Source.is_active == 1).all()
            for source in sources:
                if source.type == "rss":
                    rss_collector.collect(db, source)
            logger.info("Cycle complete.")
        except Exception as e:
            logger.error(f"Scheduler error: {e}")
        finally:
            db.close()

        time.sleep(15 * 60) # 15 minutes

if __name__ == "__main__":
    run_scheduler()
