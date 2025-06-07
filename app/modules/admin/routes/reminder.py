from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database.database import get_db
from app.modules.user.deps import get_current_user
from app.modules.reminder.schema import ReminderCreate, ReminderResponse
from app.modules.reminder.routes import (
    create_reminder_db,
    get_reminders_by_user_id_db,
    get_reminder_by_id_db,
    update_reminder_db,
    delete_reminder_db
)
from app.rbac import require_role

admin_reminder_router = APIRouter(
    prefix="/reminders",
    tags=["Admin Reminders"],
    dependencies=[Depends(require_role(["Admin"]))]
)

@admin_reminder_router.post("/", response_model=ReminderResponse)
def admin_create_reminder(
    reminder_data: ReminderCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return create_reminder_db(db, reminder_data)

@admin_reminder_router.get("/user/{user_id}", response_model=List[ReminderResponse])
def admin_get_reminders_by_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return get_reminders_by_user_id_db(db, user_id)

@admin_reminder_router.put("/{reminder_id}", response_model=ReminderResponse)
def admin_update_reminder(
    reminder_id: int,
    reminder_data: ReminderCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    updated = update_reminder_db(db, reminder_id, reminder_data)
    if not updated:
        raise HTTPException(status_code=404, detail="Reminder not found.")
    return updated

@admin_reminder_router.delete("/{reminder_id}", status_code=204)
def admin_delete_reminder(
    reminder_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    success = delete_reminder_db(db, reminder_id)
    if not success:
        raise HTTPException(status_code=404, detail="Reminder not found.")
    return