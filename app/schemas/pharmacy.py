from pydantic import BaseModel
from typing import Optional

class PharmacyBase(BaseModel):
    name: str
    description: Optional[str] = None
