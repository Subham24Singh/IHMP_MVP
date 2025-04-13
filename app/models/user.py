from sqlalchemy import Column, Integer, String, Enum
from sqlalchemy.orm import relationship
from app.database.database import Base
from app.models.enums import RoleEnum

class User(Base):
    __tablename__ = 'users'
    user_id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    phone_number = Column(String(20))
    role = Column(Enum(RoleEnum), nullable=False)
    appointments_as_patient = relationship("Appointment", foreign_keys="[Appointment.patient_id]", back_populates="patient")
    allergies = relationship("AllergyTracking", back_populates="user")
    appointments_as_doctor = relationship("Appointment", foreign_keys="[Appointment.doctor_id]", back_populates="doctor")