from pydantic import BaseModel
from datetime import datetime
from typing import Dict, Any

class DiagnosticInsightsSchema(BaseModel):
    user_id: int
    insights: Dict[str, Any]
    generated_at: datetime = datetime.utcnow()

    class Config:
        orm_mode = True