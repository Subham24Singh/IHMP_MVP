from pydantic import BaseModel
from typing import Optional

class PrescriptionCreate(BaseModel):
    patient_id: int
    doctor_id: int
    medication: str
    dosage: str

class PrescriptionResponse(PrescriptionCreate):
    prescription_id: int

    class Config:
        orm_mode = True