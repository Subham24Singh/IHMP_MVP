from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.models import Reminder, User
from app.schemas import ReminderSchema
from app.database.database import SessionLocal

router = APIRouter()
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/")
def add_reminder(reminder: ReminderSchema, db: Session = Depends(get_db)):
    # Check if user exists
    user = db.query(User).filter(User.user_id == reminder.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    new_reminder = Reminder(
        user_id=reminder.user_id,
        reminder_text=reminder.reminder_text,
        reminder_time=reminder.reminder_time
    )
    db.add(new_reminder)
    db.commit()
    db.refresh(new_reminder)
    return {"message": "Reminder added", "reminder_id": new_reminder.reminder_id}

@router.get("/{user_id}")
def get_reminders(user_id: int, db: Session = Depends(get_db)):
    reminders = db.query(Reminder).filter(Reminder.user_id == user_id).all()
    if not reminders:
        raise HTTPException(status_code=404, detail="No reminders found")
    return {"reminders": reminders}