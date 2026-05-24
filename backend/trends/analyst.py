import requests
import os
from backend.api.main import settings

class AIAnalyst:
    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.base_url = "https://api.openai.com/v1"

    def summarize_trend(self, trend_name, articles):
        # Mocking LLM call for now
        context = "\n".join([a.title for a in articles[:5]])
        return f"The trend '{trend_name}' is driven by recent updates in India regarding {context[:100]}..."

    def generate_daily_report(self, trends):
        report = "Daily Trend Intelligence Report - India\n\n"
        for t in trends[:5]:
            report += f"- {t['trend']}: Strength {t['strength']}\n"
        return report

    def synthesize_insight(self, topic):
        # Heuristic synthesis: combine top 3 signal titles into an insight
        top_signals = sorted(topic.signals, key=lambda s: s.impact_score if s.impact_score else 0, reverse=True)[:3]
        titles = [s.title for s in top_signals]
        return f"Intelligence Insight: {topic.name} is accelerating primarily due to: {', '.join(titles)}. This indicates a shift in regional demand patterns."
