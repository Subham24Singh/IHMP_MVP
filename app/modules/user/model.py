
from sqlalchemy import Column, Integer, String, Enum
from app.modules.enum.models import RoleEnum
from app.database.base import Base
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    phone_number = Column(String, unique=True)
    role = Column(Enum(RoleEnum))
    registration_number = Column(String, nullable=True)  
    
    # <-- Add this line
    appointments_as_patient = relationship(
        "Appointment",
        back_populates="patient",
        foreign_keys="Appointment.patient_id"
    )
    appointments_as_doctor = relationship(
        "Appointment",
        back_populates="doctor",
        foreign_keys="Appointment.doctor_id"
    )

    allergies = relationship(
        "AllergyTracking",
        back_populates="user",
        cascade="all, delete-orphan"
    )