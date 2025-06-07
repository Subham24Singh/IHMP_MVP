from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database.database import get_db
from app.modules.doctor.deps import get_current_doctor
from app.modules.reminder.schema import ReminderResponse
from app.modules.reminder.routes import get_reminders_by_user_id_db
from app.modules.doctor.utils import has_appointment_with_patient
from app.rbac import require_role

doctor_reminder_router = APIRouter(
    prefix="/reminders",
    tags=["Doctor Reminders"],
    dependencies=[Depends(require_role(["Doctor"]))]
)

@doctor_reminder_router.get("/patient/{patient_id}", response_model=List[ReminderResponse])
def get_patient_reminders(
    patient_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_doctor)
):
    if not has_appointment_with_patient(db, doctor_id=current_user.user_id, patient_id=patient_id):
        raise HTTPException(status_code=403, detail="No appointment with this patient.")
    return get_reminders_by_user_id_db(db, patient_id)