from pydantic import BaseModel
from app.models.enums import RoleEnum

class UserSchema(BaseModel):
    username: str
    email: str
    hashed_password: str
    phone_number: str
    role: RoleEnum

    class Config:
        orm_mode = True