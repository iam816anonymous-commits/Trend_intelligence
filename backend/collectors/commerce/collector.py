from backend.collectors.base import BaseCollector
import datetime

class CommerceCollector(BaseCollector):
    def collect(self, db):
        # Simulating commerce movement signals for Tier-2/3 India
        signals = [
            {
                "title": "Indore: Zepto inventory low on cooling fans",
                "body": "Availability drop of 60% in Indore central hub.",
                "source": "zepto",
                "url": f"https://zepto.com/alert/{datetime.datetime.now().timestamp()}_1",
                "category": "Appliances",
                "region": "Indore",
                "type": "commerce"
            },
            {
                "title": "Ahmedabad: Blinkit spike in ORS & Hydration",
                "body": "Daily sales volume exceeded peak summer average by 40%.",
                "source": "blinkit",
                "url": f"https://blinkit.com/alert/{datetime.datetime.now().timestamp()}_2",
                "category": "Healthcare",
                "region": "Ahmedabad",
                "type": "commerce"
            }
        ]
        return self.save_signals(db, signals)
