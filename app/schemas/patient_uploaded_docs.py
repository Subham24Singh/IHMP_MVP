from pydantic import BaseModel
from datetime import datetime
from typing import Dict, Any

class PatientUploadedDocsSchema(BaseModel):
    user_id: int
    document_data: Dict[str, Any]
    uploaded_at: datetime = datetime.utcnow()

    class Config:
        orm_mode = True