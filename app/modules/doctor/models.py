from sqlalchemy import ARRAY, Column, Integer, String, ForeignKey, Date, Time, Enum, Text, DateTime, Float
from sqlalchemy.orm import relationship
from app.database.database import Base
import enum

# Enum for AvailabilitySlot status
class SlotStatus(enum.Enum):
    AVAILABLE = "available"
    BOOKED = "booked"
    UNAVAILABLE = "unavailable"

# Doctor model
class Doctor(Base):
    __tablename__ = "doctors"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), unique=True, nullable=False)
    full_name = Column(String, nullable=False)
    specialty = Column(String, nullable=False)
    bio = Column(String)
    education = Column(String)
    experience = Column(String)
    clinic_address = Column(String)
    photo_url = Column(String)
    available_days = Column(ARRAY(String))
    time_slots = Column(String)
    average_rating = Column(Float, nullable=False, default=0.0)
    total_ratings = Column(Integer, nullable=False, default=0)

    certifications = Column(String)
    languages_spoken = Column(ARRAY(String))
    fees = Column(Float)
    insurance_accepted = Column(Integer)  # 0 = False, 1 = True
    areas_of_expertise = Column(String)
    
    # Relationships
    availability_slots = relationship("AvailabilitySlot", back_populates="doctor", cascade="all, delete-orphan")
    reviews = relationship("Review", back_populates="doctor", cascade="all, delete-orphan")
    specialties = relationship("DoctorSpecialty", back_populates="doctor", cascade="all, delete-orphan")

# AvailabilitySlot model
class AvailabilitySlot(Base):
    __tablename__ = "availability_slots"

    slot_id = Column(Integer, primary_key=True, index=True)
    doctor_id = Column(Integer, ForeignKey("doctors.id"), nullable=False)
    slot_date = Column(Date, nullable=False)
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
    status = Column(Enum(SlotStatus), default=SlotStatus.AVAILABLE, nullable=False)

    doctor = relationship("Doctor", back_populates="availability_slots")

# Review model
class Review(Base):
    __tablename__ = "reviews"

    review_id = Column(Integer, primary_key=True, index=True)
    doctor_id = Column(Integer, ForeignKey("doctors.id"), nullable=False)
    patient_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    rating = Column(Integer, nullable=False)
    review_text = Column(Text, nullable=True)
    review_date = Column(DateTime, nullable=False)

    doctor = relationship("Doctor", back_populates="reviews")
    patient = relationship("User")

# Specialty model (optional)
class Specialty(Base):
    __tablename__ = "specialties"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)

# DoctorSpecialty join table (optional)
class DoctorSpecialty(Base):
    __tablename__ = "doctor_specialties"

    doctor_id = Column(Integer, ForeignKey("doctors.id"), primary_key=True)
    specialty_id = Column(Integer, ForeignKey("specialties.id"), primary_key=True)
    doctor = relationship("Doctor", back_populates="specialties")
    specialty = relationship("Specialty", back_populates="doctors")

# Add the missing relationship in the Specialty model
Specialty.doctors = relationship(
    "DoctorSpecialty", back_populates="specialty", cascade="all, delete-orphan"
)
