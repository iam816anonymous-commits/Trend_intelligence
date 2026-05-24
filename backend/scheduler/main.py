import logging
import json
from backend.storage.models import SessionLocal
from backend.scheduler.task_manager import TaskManager

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("Worker")

def run_pulse():
    manager = TaskManager()
    try:
        logger.info("Starting Pulse Cycle [Ingestion -> Clustering -> Synthesis]")

        manager.run_collection_task()
        manager.run_clustering_task()
        manager.run_opportunity_task()

        logger.info("Pulse Cycle Complete.")
    except Exception as e:
        logger.error(f"Pulse Cycle Failed: {e}", exc_info=True)
    finally:
        manager.close()

if __name__ == "__main__":
    import time
    while True:
        run_pulse()
        time.sleep(900) # 15 minutes
