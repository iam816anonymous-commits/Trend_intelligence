from backend.storage.models import Topic, Knowledge, LearningLog, Signal
from sqlalchemy.orm import Session
from sqlalchemy import func
import datetime

class LearningService:
    def __init__(self, db: Session):
        self.db = db

    def extract_new_knowledge(self):
        """Analyze high-confidence topics to learn new market concepts"""
        topics = self.db.query(Topic).filter(Topic.confidence > 0.8).all()
        new_items = []

        for topic in topics:
            existing = self.db.query(Knowledge).filter(Knowledge.concept == topic.name).first()
            if not existing:
                item = Knowledge(
                    concept=topic.name,
                    definition=f"Market concept synthesized from trend: {topic.name}",
                    category="Emerging Market",
                    strength=topic.trend_score
                )
                self.db.add(item)
                new_items.append(item)

                # Log the learning event
                log = LearningLog(
                    action=f"Learned new concept: {topic.name}",
                    impact_area="Taxonomy Expansion"
                )
                self.db.add(log)

        self.db.commit()
        return new_items

    def suggest_taxonomy_expansion(self):
        """Analyze signals without a clear category to suggest new ones"""
        # Find recurring regions in non-assigned signals
        unassigned_regions = self.db.query(Signal.region, func.count(Signal.id))\
            .filter(Signal.topic_id == None)\
            .group_by(Signal.region)\
            .having(func.count(Signal.id) > 10)\
            .all()

        for region, count in unassigned_regions:
            # Check if region is a 'rising star' to be learned
            log = LearningLog(
                action=f"Suggested new regional focus: {region} (Signal density: {count})",
                impact_area="Geo Taxonomy"
            )
            self.db.add(log)

        self.db.commit()
