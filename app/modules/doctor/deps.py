from fastapi import Depends, HTTPException, status
from app.modules.user.deps import get_current_user
from app.modules.user.model import User
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.modules.doctor.models import Doctor
from app.modules.appointment.model import Appointment

def get_current_doctor(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> Doctor:
    if current_user.role != "Doctor":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only doctors are allowed to access this route",
        )

    doctor = db.query(Doctor).filter(Doctor.user_id == current_user.user_id).first()
    if not doctor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Doctor profile not found",
        )

    return doctor

def verify_doctor_patient_link(doctor_id: int, patient_id: int, db: Session):
    appointment = db.query(Appointment).filter_by(doctor_id=doctor_id, patient_id=patient_id).first()
    if not appointment:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied. No patient relationship found."
        )


def check_doctor_appointment(db: Session, doctor_id: int, appointment_id: int):
    appointment = db.query(Appointment).filter(Appointment.id == appointment_id, Appointment.doctor_id == doctor_id).first()
    if not appointment:
        raise HTTPException(status_code=403, detail="You are not authorized for this appointment")
    return appointment