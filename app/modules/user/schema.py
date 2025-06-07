from typing import Optional
from pydantic import BaseModel
# from app.modules.enum.models import RoleEnum  # No longer needed for schema

class UserSchema(BaseModel):
    username: str
    email: str
    password: str
    phone_number: Optional[str] = None
    role: str  # Accept as string
    registration_number: Optional[str] = None

    class Config:
        from_attributes = True