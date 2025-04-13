from pydantic import BaseModel
from datetime import datetime
from typing import Dict, Any

class FollowupRecommendationsSchema(BaseModel):
    user_id: int
    recommendations: Dict[str, Any]
    recommended_at: datetime = datetime.utcnow()

    class Config:
        orm_mode = True