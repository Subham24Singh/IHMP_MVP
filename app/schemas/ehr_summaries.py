from pydantic import BaseModel
from datetime import datetime
from typing import Dict, Any

class EHRSummarySchema(BaseModel):
    user_id: int
    ehr_data: Dict[str, Any]
    updated_at: datetime = datetime.utcnow()

    class Config:
        orm_mode = True