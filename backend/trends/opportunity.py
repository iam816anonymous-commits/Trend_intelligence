from backend.storage.models import Topic, Opportunity
from sqlalchemy.orm import Session
import random

class OpportunityFinder:
    def __init__(self, db: Session):
        self.db = db

    def categorize_opp(self, topic_name):
        # Heuristic categorization
        topic_lower = topic_name.lower()
        if any(w in topic_lower for w in ['drink', 'sachet', 'bottle', 'food', 'towel']):
            return "D2C"
        if any(w in topic_lower for w in ['software', 'app', 'tool', 'ai']):
            return "SaaS"
        return "Service"

    def find_opportunities(self):
        # 1. Fetch High Growth Topics
        topics = self.db.query(Topic).filter(Topic.trend_score > 30).all()

        opportunities = []
        for topic in topics:
            existing = self.db.query(Opportunity).filter(Opportunity.market_niche == topic.name).first()
            if existing:
                continue

            opp_type = self.categorize_opp(topic.name)
            opp = Opportunity(
                title=f"Launch {topic.name} {opp_type}",
                description=f"Market intelligence shows significant signal clusters in {topic.name} across Tier-2 India.",
                market_niche=topic.name,
                type=opp_type,
                evidence_score=topic.trend_score,
                launch_cost_est=random.choice([200000, 500000, 800000, 1500000]),
                signals_count=len(topic.signals),
                potential_roi="High" if topic.trend_score > 70 else "Medium"
            )
            self.db.add(opp)
            opportunities.append(opp)

        self.db.commit()
        return opportunities
