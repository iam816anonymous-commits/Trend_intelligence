from backend.storage.models import Topic, Opportunity
from sqlalchemy.orm import Session
import random

class OpportunityFinder:
    def __init__(self, db: Session):
        self.db = db

    def synthesize_roadmap(self, topic):
        # Generate execution steps based on signal types
        types = set([s.type for s in topic.signals])
        roadmap = ["Market validation with Google Trends"]
        if 'commerce' in types:
            roadmap.append("Competitor inventory tracking on Zepto/Blinkit")
        if 'consumer' in types:
            roadmap.append("Direct consumer sentiment analysis on Reddit/X")
        roadmap.append("Low-cost MVP launch via Instagram ads")
        return roadmap

    def find_opportunities(self):
        # Look for topics with high growth and high confidence
        topics = self.db.query(Topic).filter(Topic.trend_score > 40, Topic.confidence > 0.5).all()

        opportunities = []
        for topic in topics:
            existing = self.db.query(Opportunity).filter(Opportunity.market_niche == topic.name).first()
            if existing: continue

            opp = Opportunity(
                title=f"Opportunity: {topic.name}",
                description=f"Automated synthesis of {len(topic.signals)} signals shows high demand in {topic.name}.",
                market_niche=topic.name,
                type="D2C" if "demand" in topic.name.lower() else "SaaS",
                evidence_score=topic.trend_score,
                launch_cost_est=random.choice([100000, 300000, 700000]),
                signals_count=len(topic.signals),
                potential_roi="High" if topic.trend_score > 60 else "Medium",
                execution_roadmap=self.synthesize_roadmap(topic)
            )
            self.db.add(opp)
            opportunities.append(opp)

        self.db.commit()
        return opportunities
