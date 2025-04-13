from pydantic import BaseModel
from typing import Optional

class DoctorBase(BaseModel):
    name: str
    description: Optional[str] = None
