from pydantic import BaseModel
from typing import Optional

class RecoveryBase(BaseModel):
    name: str
    description: Optional[str] = None
