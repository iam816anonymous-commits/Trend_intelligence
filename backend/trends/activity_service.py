from sqlalchemy.orm import Session
from backend.storage.models import AgentActivity
import datetime

class ActivityService:
    def __init__(self, db: Session):
        self.db = db

    def log(self, task_name: str, status: str, message: str, metadata: dict = None):
        activity = AgentActivity(
            task_name=task_name,
            status=status,
            message=message,
            metadata_json=metadata or {}
        )
        self.db.add(activity)
        self.db.commit()
        return activity
