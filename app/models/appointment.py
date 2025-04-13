from sqlalchemy import Column, Integer, DateTime, Enum, ForeignKey,String
from sqlalchemy.orm import relationship
from app.database.database import Base
from app.models.enums import StatusEnum


class Appointment(Base):
     __tablename__ = "appointments"
     appointment_id = Column(Integer, primary_key=True, index=True)
     patient_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"))
     doctor_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"))
     appointment_date = Column(DateTime, nullable=False)
     status = Column(String(50), nullable=False, default="Scheduled")
     patient = relationship("User", foreign_keys=[patient_id], back_populates="appointments_as_patient")
     doctor = relationship("User", foreign_keys=[doctor_id], back_populates="appointments_as_doctor")