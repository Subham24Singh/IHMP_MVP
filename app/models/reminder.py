from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from app.database.database import Base

class Reminder(Base):
    __tablename__ = 'reminders'
    reminder_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    reminder_text = Column(String)
    reminder_time = Column(DateTime)