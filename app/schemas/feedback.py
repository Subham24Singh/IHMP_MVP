from pydantic import BaseModel
from typing import Optional

class FeedbackBase(BaseModel):
    name: str
    description: Optional[str] = None
