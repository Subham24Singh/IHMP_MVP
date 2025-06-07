from pydantic import BaseModel
from datetime import datetime
from typing import Any

class FollowUpCreate(BaseModel):
    user_id: int
    recommendations: Any  # Use more specific type if you know the JSON structure
    recommended_at: datetime

class FollowUpResponse(FollowUpCreate):
    id: int

    class Config:
        orm_mode = True