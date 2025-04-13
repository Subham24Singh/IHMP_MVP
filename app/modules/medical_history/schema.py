from pydantic import BaseModel
from datetime import date

class MedicalHistorySchema(BaseModel):
    user_id: int
    condition: str
    treatment: str
    start_date: date
    end_date: date

    class Config:
        orm_mode = True