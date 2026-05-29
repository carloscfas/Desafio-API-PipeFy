from sqlalchemy import Column, String, DateTime
from app.db.session import Base
import datetime

class ProcessedEvent(Base):
    __tablename__ = "processed_events"

    event_id = Column(String, primary_key=True, index=True)
    processed_at = Column(DateTime, default=datetime.datetime.utcnow)
