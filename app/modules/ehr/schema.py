from pydantic import BaseModel
from typing import Optional, Any

class EHRCreate(BaseModel):
    user_id: int
    data: Any  # Replace with specific fields if you know the EHR structure

class EHRResponse(EHRCreate):
    id: int

    class Config:
        orm_mode = True