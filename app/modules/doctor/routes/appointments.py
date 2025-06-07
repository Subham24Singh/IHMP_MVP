from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from typing import List
import time
import logging

from app.database.database import get_db
from app.modules.doctor.deps import get_current_doctor
from app.modules.appointment.model import Appointment
from app.modules.appointment.schema import AppointmentResponse
from app.modules.user.model import User
from app.rbac import require_role

doctor_appointments_router = APIRouter(
    prefix="/appointments",
    tags=["Doctor Appointments"],
    dependencies=[Depends(require_role(["Doctor"]))]
)

# --- Simple in-memory rate limiter ---
rate_limit_cache = {}
RATE_LIMIT = 10  # max requests
RATE_PERIOD = 60  # per 60 seconds

def rate_limiter(user_id):
    now = int(time.time())
    window = now // RATE_PERIOD
    key = f"doctor:{user_id}:{window}"
    count = rate_limit_cache.get(key, 0)
    if count >= RATE_LIMIT:
        return False
    rate_limit_cache[key] = count + 1
    return True

@doctor_appointments_router.get("/", response_model=List[AppointmentResponse])
async def get_my_appointments(
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_doctor)
):
    # Rate limiting
    if not rate_limiter(current_user.user_id):
        raise HTTPException(status_code=429, detail="Rate limit exceeded. Try again later.")
    # Audit log
    logging.basicConfig(filename='audit.log', level=logging.INFO)
    logging.info(f"AUDIT: {current_user.username} accessed get_my_appointments at {time.ctime()}")
    # Per-object access control (already enforced by doctor_id filter)
    appointments = (
        db.query(Appointment)
        .filter(Appointment.doctor_id == current_user.user_id)
        .order_by(Appointment.appointment_date.desc())
        .all()
    )
    if not appointments:
        raise HTTPException(status_code=404, detail="No appointments found for this doctor.")
    return appointments