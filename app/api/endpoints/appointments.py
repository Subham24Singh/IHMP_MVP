from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.models import Appointment, User
from app.schemas import AppointmentCreate
from app.database.database import SessionLocal

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/")
def create_appointment(appointment_data: AppointmentCreate, db: Session = Depends(get_db)):
    patient = db.query(User).filter(User.user_id == appointment_data.patient_id, User.role == "Patient").first()
    doctor = db.query(User).filter(User.user_id == appointment_data.doctor_id, User.role == "Doctor").first()

    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")

    appointment = Appointment(
        patient_id=patient.user_id,
        doctor_id=doctor.user_id,
        appointment_date=appointment_data.appointment_date,
        status="Scheduled"
    )
    db.add(appointment)
    db.commit()
    db.refresh(appointment)
    return {"message": "Appointment created", "appointment_id": appointment.appointment_id}

@router.get("/{doctor_id}")
def get_appointments(doctor_id: int, db: Session = Depends(get_db)):
    doctor = db.query(User).filter(User.user_id == doctor_id, User.role == "Doctor").first()
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")

    appointments = db.query(Appointment).filter(Appointment.doctor_id == doctor_id).all()

    if not appointments:
        return {"message": "No appointments found for this doctor"}

    return {"doctor_id": doctor_id, "appointments": appointments}