import re

class SignalEnricher:
    def calculate_sentiment(self, text):
        # Basic rule-based sentiment for Phase 0 improvisation
        positive_words = {'growth', 'rise', 'excellent', 'demand', 'hot', 'success'}
        negative_words = {'crisis', 'fall', 'shortage', 'bad', 'drop', 'out of stock'}

        text_lower = text.lower()
        score = 0.0
        for word in positive_words:
            if word in text_lower: score += 0.2
        for word in negative_words:
            if word in text_lower: score -= 0.2

        return max(min(score, 1.0), -1.0)

    def calculate_impact(self, signal):
        # Impact based on source weight and sentiment intensity
        weights = {'reddit': 0.6, 'blinkit': 0.9, 'news': 0.5, 'zepto': 0.9}
        base_weight = weights.get(signal.source, 0.4)

        sentiment_abs = abs(signal.sentiment)
        impact = base_weight * (1 + sentiment_abs)
        return min(impact, 1.0)

    def enrich(self, signal):
        signal.sentiment = self.calculate_sentiment(signal.title + " " + (signal.body or ""))
        signal.impact_score = self.calculate_impact(signal)
        return signal
