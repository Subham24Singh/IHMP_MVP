from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ReminderCreate(BaseModel):
    user_id: int
    reminder_text: str
    reminder_time: datetime

class ReminderResponse(ReminderCreate):
    id: int

    class Config:
        orm_mode = True