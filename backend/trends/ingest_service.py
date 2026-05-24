import logging
from sqlalchemy.ext.asyncio import AsyncSession
from backend.storage.models import Signal
from sqlalchemy import select

logger = logging.getLogger("IngestService")

class SignalIngestService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def ingest_batch(self, signals_data: list[dict]):
        """B2B production batch ingestion with deduplication check"""
        new_signals = []
        for data in signals_data:
            # Check for existing URL
            stmt = select(Signal).where(Signal.url == data["url"])
            result = await self.db.execute(stmt)
            if not result.scalar_one_or_none():
                sig = Signal(**data)
                self.db.add(sig)
                new_signals.append(sig)

        if new_signals:
            await self.db.commit()
            logger.info(f"Ingested {len(new_signals)} new signals.")
        return new_signals
