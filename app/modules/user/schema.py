

from typing import Optional
from pydantic import BaseModel, EmailStr

class UserBaseSchema(BaseModel):
    username: str
    email: EmailStr
    phone_number: Optional[str] = None

class PatientRegisterInput(UserBaseSchema):
    password: str
    confirm_password: str

class DoctorRegisterInput(UserBaseSchema):
    password: str
    confirm_password: str
    registration_number: str

class UserOutputSchema(UserBaseSchema):
    user_id: int
    role: str

    class Config:
        from_attributes = True