from backend.storage.models import Topic, Opportunity
from sqlalchemy.orm import Session

class OpportunityFinder:
    def find_opportunities(self, db: Session, budget: float = 1000000):
        # 1. Fetch High Growth/Early Topics
        topics = db.query(Topic).filter(Topic.trend_score > 50).all()

        opportunities = []
        for topic in topics:
            # Logic to derive opportunity from topic
            # This would normally use an LLM
            opp = Opportunity(
                title=f"Business in {topic.name}",
                description=f"Based on rising trend score of {topic.trend_score}",
                market_niche=topic.name,
                evidence_score=topic.trend_score,
                launch_cost_est=budget * 0.8,
                signals_count=10 # placeholder
            )
            opportunities.append(opp)

        return opportunities
