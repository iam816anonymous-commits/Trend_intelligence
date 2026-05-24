from sqlalchemy.orm import Session
from backend.storage.models import Signal
from collections import Counter

class GeoEngine:
    def __init__(self, db: Session):
        self.db = db

    def get_tier2_rising_stars(self):
        # Tier-2/3 cities list
        tier2_cities = ['Indore', 'Vizag', 'Vijayawada', 'Coimbatore', 'Ahmedabad', 'Pune', 'Lucknow', 'Jaipur']

        signals = self.db.query(Signal).filter(Signal.region.in_(tier2_cities)).all()

        city_stats = {}
        for city in tier2_cities:
            city_signals = [s for s in signals if s.region == city]
            if not city_signals: continue

            # Categories in this city
            categories = Counter([s.category for s in city_signals]).most_common(3)

            city_stats[city] = {
                "signal_count": len(city_signals),
                "top_categories": [c[0] for c in categories],
                "pulse_score": min(len(city_signals) * 5, 100)
            }

        return city_stats
