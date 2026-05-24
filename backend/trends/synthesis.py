from backend.storage.models import Topic

class SynthesisEngine:
    def __init__(self, db):
        self.db = db

    def find_correlations(self):
        # High-level synthesis logic
        topics = self.db.query(Topic).all()
        correlations = []

        for i, topic_a in enumerate(topics):
            for topic_b in topics[i+1:]:
                # Heuristic: Match keywords or signal overlap
                # For Phase 0, we look for region/category overlap
                regions_a = set([s.region for s in topic_a.signals])
                regions_b = set([s.region for s in topic_b.signals])

                overlap = regions_a.intersection(regions_b)
                if overlap:
                    correlations.append({
                        "topic_a": topic_a.name,
                        "topic_b": topic_b.name,
                        "type": "Regional Coupling",
                        "reason": f"Both trends accelerating in {list(overlap)[0]}"
                    })

        return correlations
