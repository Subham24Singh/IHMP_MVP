from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class DoctorBase(BaseModel):
    full_name: str
    specialty: str
    bio: Optional[str] = None
    education: Optional[str] = None
    experience: Optional[str] = None
    clinic_address: Optional[str] = None
    photo_url: Optional[str] = None
    available_days: List[str]
    time_slots: str
    average_rating: float
    total_reviews: int

    class Config:
        from_attributes = True

class DoctorResponse(DoctorBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True
