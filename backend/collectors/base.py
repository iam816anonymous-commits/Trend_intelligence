import abc
from sqlalchemy.orm import Session
from backend.storage.models import Signal

class BaseCollector(abc.ABC):
    @abc.abstractmethod
    def collect(self, db: Session) -> list[Signal]:
        pass

    def save_signals(self, db: Session, signal_data_list: list[dict]):
        saved = []
        for data in signal_data_list:
            existing = db.query(Signal).filter(Signal.url == data["url"]).first()
            if not existing:
                signal = Signal(**data)
                db.add(signal)
                saved.append(signal)
        db.commit()
        return saved
