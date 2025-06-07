from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database.database import get_db
from app.modules.user.deps import get_current_patient
from app.modules.appointment.model import Appointment
from app.modules.appointment.schema import AppointmentResponse
from app.modules.user.model import User
from app.rbac import require_role

patient_appointments_router = APIRouter(
    prefix="/appointments",
    tags=["Patient Appointments"],
    dependencies=[Depends(require_role(["Patient"]))]
)

@patient_appointments_router.get("/", response_model=List[AppointmentResponse])
async def get_my_appointments(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_patient)
):
    appointments = (
        db.query(Appointment)
        .filter(Appointment.patient_id == current_user.user_id)
        .order_by(Appointment.appointment_date.desc())
        .all()
    )
    if not appointments:
        raise HTTPException(status_code=404, detail="No appointments found for this patient.")
    return appointments