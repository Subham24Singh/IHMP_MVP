from pydantic import BaseModel
from datetime import datetime
from typing import Dict, Any

class AITranscriptionsSchema(BaseModel):
    user_id: int
    transcription_data: Dict[str, Any]
    created_at: datetime = datetime.utcnow()

    class Config:
        orm_mode = True