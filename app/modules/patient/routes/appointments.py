# app/modules/patient/routes/appointments.py (or wherever patient_appointments_router is defined)

import logging
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime, timedelta, timezone
import pytz # Import pytz for timezone handling

from app.database.database import get_db
from app.modules.doctor.routes.model import Doctor
from app.modules.doctor.schema import DoctorResponse
from app.modules.user.deps import get_current_patient
from app.modules.appointment.model import Appointment
from app.modules.appointment.schema import AppointmentResponse, AppointmentCreate
from app.modules.user.model import User
from app.rbac import require_role
from app.config import settings # Import settings

patient_appointments_router = APIRouter(
    prefix="/appointments",
    tags=["Patient Appointments"],
    dependencies=[Depends(require_role(["Patient"]))]
)

# Helper function to get current time in a timezone-aware manner
def get_current_timezone_aware_time():
    tz = pytz.timezone(settings.TIMEZONE)
    return datetime.now(tz)

@patient_appointments_router.get("/", response_model=List[AppointmentResponse])
async def get_my_appointments(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_patient)
):
    """
    Retrieves all appointments for the authenticated patient, ordered by date.
    """
    appointments = (
        db.query(Appointment)
        .filter(
            Appointment.patient_id == current_user.user_id,
            Appointment.status != "Cancelled"
        )
        .order_by(Appointment.appointment_date.desc())
        .all()
    )
    if not appointments:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No appointments found for this patient.")
    return appointments

@patient_appointments_router.get("/doctors", response_model=List[DoctorResponse])
async def get_doctors(
    db: Session = Depends(get_db)
):
    """
    Retrieves all doctors with their ratings and availability.
    """
    doctors = db.query(Doctor).all()
    return doctors

@patient_appointments_router.delete("/{appointment_id}/", status_code=204)
async def cancel_appointment(
    appointment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_patient)
):
    """
    Securely cancel (mark as cancelled) an appointment for the authenticated patient only.
    """
    appointment = db.query(Appointment).filter(
        Appointment.appointment_id == appointment_id,
        Appointment.patient_id == current_user.user_id
    ).first()
    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found.")
    appointment.status = "Cancelled"
    db.commit()
    return {"detail": "Appointment cancelled."}

@patient_appointments_router.patch("/{appointment_id}/", response_model=AppointmentResponse)
async def reschedule_appointment(
    appointment_id: int,
    update_data: AppointmentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_patient)
):
    """
    Securely reschedule an appointment for the authenticated patient only.
    """
    appointment = db.query(Appointment).filter(
        Appointment.appointment_id == appointment_id,
        Appointment.patient_id == current_user.user_id,
        Appointment.status != "Cancelled"
    ).first()
    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found or has been cancelled.")
    # Optionally: validate the new date/time as in create_appointment
    appointment.appointment_date = update_data.appointment_date
    appointment.status = "Scheduled"
    db.commit()
    db.refresh(appointment)
    return appointment

@patient_appointments_router.post("/", response_model=AppointmentResponse, status_code=status.HTTP_201_CREATED)
async def create_appointment(
    appointment_data: AppointmentCreate, # The data sent by the patient
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_patient) # The patient creating the appointment
):
    """
    Allows an authenticated patient to create a new appointment with a specific doctor.
    Ensures secure creation, preventing unauthorized bookings and enforcing business rules.
    """
    # --- Z+ Security & Patient-Specific Booking Enforcement ---

    # 1. User can only create their own appointment (Already handled by get_current_patient implicitly)
    #    The `patient_id` for the new appointment will be `current_user.user_id`,
    #    which is derived from the authenticated token. A malicious user cannot
    #    forge a `patient_id` in the request body because it's not taken from there.
    #    This is fundamental to token-based authentication and is already secure.

    # 2. Validate the doctor_id:
    #    Ensure the doctor exists and has the 'Doctor' role.
    #    This prevents booking with non-existent users or users not marked as doctors.
    doctor = db.query(User).filter(User.user_id == appointment_data.doctor_id, User.role == "Doctor").first()
    if not doctor:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Doctor not found or is not a valid doctor.")

    # 3. Timezone-aware Date/Time Validation (Fixes the TypeError)
    #    Convert the incoming appointment date to a timezone-aware object for comparison.
    #    It's best practice to store dates in UTC in the database, but compare with server's timezone.
    current_time_aware = get_current_timezone_aware_time()

    # If appointment_data.appointment_date is naive (no timezone info), make it aware.
    # Assuming appointment_date from client is in ISO 8601 format with or without 'Z' for UTC.
    # Pydantic's datetime parsing usually handles 'Z' for UTC aware, but if not,
    # it will be naive. Let's ensure consistent timezone handling.
    if appointment_data.appointment_date.tzinfo is None:
        # If naive, assume it's in the server's configured timezone and make it aware
        local_tz = pytz.timezone(settings.TIMEZONE)
        appointment_date_aware = local_tz.localize(appointment_data.appointment_date)
    else:
        # If already timezone-aware, convert to server's timezone for comparison
        appointment_date_aware = appointment_data.appointment_date.astimezone(pytz.timezone(settings.TIMEZONE))

    # Check if the appointment date/time is in the future relative to server's current time
    if appointment_date_aware <= current_time_aware:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Appointment date and time must be in the future. Current server time: {current_time_aware.isoformat()}"
        )

    # 4. Doctor's Availability Check (Z+ Secure: Prevents double-booking)
    #    Check if the doctor is already booked at that exact time.
    #    Consider potential time zone conversions if your DB stores in UTC and input is local.
    #    For robust comparison, ensure both datetimes are standardized (e.g., to UTC)
    #    before querying the database.
    #    Assuming `appointment_date` in DB is UTC or local consistently.
    #    Let's convert client's desired time to UTC for DB query consistency if DB stores UTC.
    appointment_date_utc = appointment_data.appointment_date.astimezone(timezone.utc) if appointment_data.appointment_date.tzinfo else appointment_data.appointment_date.replace(tzinfo=timezone.utc)

    existing_appointment = db.query(Appointment).filter(
        Appointment.doctor_id == appointment_data.doctor_id,
        # For exact time slot, compare directly. For flexible slots, use range queries.
        Appointment.appointment_date == appointment_date_utc, # Compare with UTC
        Appointment.status.in_(["Scheduled", "Confirmed"]) # Only check active appointments
    ).first()

    if existing_appointment:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Doctor is already booked at this exact time.")

    # Additional Security/Business Rules:

    # 5. Prevent booking too far in the future/past (e.g., only next 3 months)
    max_booking_date = current_time_aware + timedelta(days=90) # Requires `from datetime import timedelta`
    if appointment_date_aware > max_booking_date:
         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Appointments can only be booked up to 3 months in advance.")

    # 6. Doctor's Working Hours (more complex, but essential for real apps)
    #    You'd typically have a `DoctorAvailability` model/table.
    #    Example:
    #    availability = db.query(DoctorAvailability).filter(
    #        DoctorAvailability.doctor_id == appointment_data.doctor_id,
    #        DoctorAvailability.day_of_week == appointment_date_aware.weekday(),
    #        DoctorAvailability.start_time <= appointment_date_aware.time(),
    #        DoctorAvailability.end_time >= (appointment_date_aware + timedelta(minutes=30)).time() # Assuming 30 min slots
    #    ).first()
    #    if not availability:
    #        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Doctor is not available at this time.")

    # --- Create the Appointment ---
    new_appointment = Appointment(
        patient_id=current_user.user_id, # This is the "Z+ secure" part for patient_id
        doctor_id=appointment_data.doctor_id,
        appointment_date=appointment_date_utc, # Store in UTC
        status="Scheduled" # Default status when created by patient
    )

    try:
        db.add(new_appointment)
        db.commit()
        db.refresh(new_appointment)
        return new_appointment
    except Exception as e:
        db.rollback()
        # Log the full exception for debugging, but return a generic error to client
        import traceback
        logging.error(f"Error creating appointment: {traceback.format_exc()}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An unexpected error occurred while creating the appointment.")