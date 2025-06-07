from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database.database import get_db
from app.modules.user.deps import get_current_patient
from app.modules.reminder.schema import ReminderCreate, ReminderResponse
from app.modules.reminder.routes import (
    create_reminder_db,
    get_reminders_by_user_id_db,
    get_reminder_by_id_db,
    update_reminder_db,
    delete_reminder_db
)
from app.rbac import require_role

patient_reminder_router = APIRouter(
    prefix="/reminders",
    tags=["Patient Reminders"],
    dependencies=[Depends(require_role(["Patient"]))]
)

@patient_reminder_router.post("/", response_model=ReminderResponse)
def create_reminder(
    reminder_data: ReminderCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_patient)
):
    if reminder_data.user_id != current_user.user_id:
        raise HTTPException(status_code=403, detail="You can only create your own reminders.")
    return create_reminder_db(db, reminder_data)

@patient_reminder_router.get("/", response_model=List[ReminderResponse])
def get_my_reminders(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_patient)
):
    return get_reminders_by_user_id_db(db, current_user.user_id)