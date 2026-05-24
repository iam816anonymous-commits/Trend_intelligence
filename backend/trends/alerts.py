import requests
import os

class AlertEngine:
    def __init__(self):
        self.webhook_url = os.getenv("ALERT_WEBHOOK_URL")

    def send_alert(self, message):
        if not self.webhook_url:
            print(f"ALERT: {message}")
            return

        try:
            requests.post(self.webhook_url, json={"text": message})
        except Exception as e:
            print(f"Failed to send alert: {e}")

    def check_and_alert(self, trend):
        if trend['strength'] > 80:
            self.send_alert(f"HIGH STRENGTH TREND DETECTED: {trend['trend']} ({trend['strength']})")
