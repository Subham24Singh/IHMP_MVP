from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional

from app.database.database import get_db
from app.modules.appointment.model import Appointment
from app.modules.appointment.schema import AppointmentResponse
from app.modules.user.model import User
from app.rbac import require_role

admin_appointments_router = APIRouter(
    prefix="/appointments",
    tags=["Admin Appointments"],
    dependencies=[Depends(require_role(["Admin"]))]
)

@admin_appointments_router.get("/", response_model=List[AppointmentResponse])
async def get_all_appointments(
    doctor_id: Optional[int] = None,
    patient_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    query = db.query(Appointment)
    if doctor_id:
        query = query.filter(Appointment.doctor_id == doctor_id)
    if patient_id:
        query = query.filter(Appointment.patient_id == patient_id)
    appointments = query.order_by(Appointment.appointment_date.desc()).all()
    return appointments

@admin_appointments_router.delete("/{appointment_id}", status_code=204)
async def delete_appointment(
    appointment_id: int,
    db: Session = Depends(get_db)
):
    appointment = db.query(Appointment).filter(Appointment.id == appointment_id).first()
    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found.")
    db.delete(appointment)
    db.commit()
    return {"detail": "Appointment deleted successfully."}