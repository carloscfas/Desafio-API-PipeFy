from pydantic import BaseModel
from datetime import datetime

class WebhookPayload(BaseModel):
    event_id: str
    card_id: str
    cliente_email: str
    timestamp: datetime
