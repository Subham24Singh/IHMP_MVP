from sqlalchemy.orm import Session
from app.modules.reminder.models import Reminder
from app.modules.reminder.schema import ReminderCreate

def create_reminder_db(db: Session, reminder_data: ReminderCreate):
    reminder = Reminder(**reminder_data.dict())
    db.add(reminder)
    db.commit()
    db.refresh(reminder)
    return reminder

def get_reminders_by_user_id_db(db: Session, user_id: int):
    return db.query(Reminder).filter(Reminder.user_id == user_id).all()

def get_reminder_by_id_db(db: Session, reminder_id: int):
    return db.query(Reminder).filter(Reminder.id == reminder_id).first()

def update_reminder_db(db: Session, reminder_id: int, reminder_data: ReminderCreate):
    reminder = db.query(Reminder).filter(Reminder.id == reminder_id).first()
    if not reminder:
        return None
    for field, value in reminder_data.dict(exclude_unset=True).items():
        setattr(reminder, field, value)
    db.commit()
    db.refresh(reminder)
    return reminder

def delete_reminder_db(db: Session, reminder_id: int):
    reminder = db.query(Reminder).filter(Reminder.id == reminder_id).first()
    if not reminder:
        return False
    db.delete(reminder)
    db.commit()
    return True