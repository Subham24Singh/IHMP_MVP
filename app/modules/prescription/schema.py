from pydantic import BaseModel

class PrescriptionSchema(BaseModel):
    patient_id: int
    doctor_id: int
    medication: str
    dosage: str

    class Config:
        orm_mode = True