from pydantic import BaseModel
from typing import Optional, List

class UserProfileResponse(BaseModel):
    user_id: int
    full_name: Optional[str] = None
    email: str
    phone_number: Optional[str] = None
    date_of_birth: Optional[str] = None
    role: str
    blood_type: Optional[str] = None
    emergency_contact: Optional[str] = None
    allergies: Optional[List[str]] = []
    chronic_conditions: Optional[List[str]] = []
    medications: Optional[List[str]] = []



class UserProfileUpdate(BaseModel):
    full_name: Optional[str] = None
    phone_number: Optional[str] = None
    date_of_birth: Optional[str] = None
    blood_type: Optional[str] = None
    emergency_contact: Optional[str] = None
    # Add other updatable fields as needed

    class Config:
        orm_mode = True