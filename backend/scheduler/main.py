import time
import logging
from backend.scheduler.task_manager import TaskManager

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("scheduler")

def main():
    manager = TaskManager()
    while True:
        try:
            manager.run_collection_task()
            manager.run_clustering_task()
            manager.run_opportunity_task()
        except Exception as e:
            logger.error(f"Scheduler loop error: {e}")

        logger.info("Sleeping for 15 minutes...")
        time.sleep(15 * 60)

if __name__ == "__main__":
    main()
