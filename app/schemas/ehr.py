from pydantic import BaseModel
from sqlalchemy.orm import relationship

class EHRSchema(BaseModel):
    patient_id: int
    diagnosis: str
    treatment: str
    notes: str

ehr = relationship("EHR", back_populates="user")

