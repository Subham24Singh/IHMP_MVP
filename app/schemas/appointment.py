from pydantic import BaseModel
from datetime import datetime
from app.models.enums import StatusEnum

class AppointmentCreate(BaseModel):
    patient_id: int
    doctor_id: int
    appointment_date: datetime

class AppointmentResponse(BaseModel):
    appointment_id: int
    patient_id: int
    doctor_id: int
    appointment_date: datetime
    status: StatusEnum

    class Config:
        orm_mode = True