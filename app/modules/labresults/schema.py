from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class LabResultCreate(BaseModel):
    user_id: int
    test_name: str
    result_value: str
    result_unit: Optional[str] = None
    result_date: datetime

class LabResultResponse(LabResultCreate):
    id: int

    class Config:
        orm_mode = True