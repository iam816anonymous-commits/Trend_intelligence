import logging
from backend.storage.models import SessionLocal, Signal
from backend.collectors.rss.collector import RSSCollector
from backend.collectors.commerce.collector import CommerceCollector
from backend.processing.enricher import SignalEnricher
from backend.trends.pulse_engine import TrendPulseEngine
from backend.trends.opportunity import OpportunityFinder
from backend.trends.learning_service import LearningService
from backend.trends.activity_service import ActivityService
from backend.trends.alerts import AlertEngine

logger = logging.getLogger("TaskManager")

class TaskManager:
    def __init__(self):
        self.db = SessionLocal()

    def run_collection_task(self):
        activity = ActivityService(self.db)
        activity.log("Collection", "executing", "Starting multi-source data collection cycle.")

        logger.info("Task: Running collection...")
        # RSS collection
        sources = [
            {"name": "The Hindu", "url": "https://www.thehindu.com/news/national/feeder/default.rss", "category": "Politics"},
            {"name": "YourStory", "url": "https://yourstory.com/feed", "category": "Startup"}
        ]
        for s in sources:
            collector = RSSCollector(s['name'], s['url'], s['category'])
            collector.collect(self.db)

        # Commerce signals
        comm_collector = CommerceCollector()
        comm_collector.collect(self.db)

        # Enrichment of new signals
        enricher = SignalEnricher()
        new_signals = self.db.query(Signal).filter(Signal.sentiment == 0.0, Signal.impact_score == 0.0).all()
        for sig in new_signals:
            enricher.enrich(sig)

        self.db.commit()
        activity.log("Collection", "success", f"Enriched {len(new_signals)} new market signals.")
        logger.info(f"Task: Collection & Enrichment complete. {len(new_signals)} signals enriched.")

    def run_clustering_task(self):
        activity = ActivityService(self.db)
        activity.log("Clustering", "thinking", "Clustering recent signals to detect emerging topics.")

        logger.info("Task: Running clustering...")
        engine = TrendPulseEngine(self.db)
        topics = engine.run()

        activity.log("Clustering", "success", f"Topic mapping complete. {len(topics)} active trends tracked.")
        logger.info(f"Task: Clustering complete. {len(topics)} topics updated.")

    def run_learning_task(self):
        logger.info("Task: Running agent self-learning cycle...")
        service = LearningService(self.db)
        learned = service.extract_new_knowledge()
        service.suggest_taxonomy_expansion()
        logger.info(f"Task: Learning complete. Agent learned {len(learned)} new concepts.")

    def run_opportunity_task(self):
        logger.info("Task: Running opportunity discovery...")
        finder = OpportunityFinder(self.db)
        opps = finder.find_opportunities()

        # Alerting on top opportunities
        alerts = AlertEngine()
        for opp in opps:
            if opp.evidence_score > 70:
                alerts.send_alert(f"🚀 HIGH IMPACT OPPORTUNITY: {opp.title} (Score: {opp.evidence_score})")

        logger.info(f"Task: Discovery complete. {len(opps)} new opportunities found.")

    def close(self):
        self.db.close()
