from pydantic import BaseModel
from datetime import datetime

class ReminderSchema(BaseModel):
    user_id: int
    reminder_text: str
    reminder_time: datetime

    class Config:
        orm_mode = True