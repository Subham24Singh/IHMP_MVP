from sqlalchemy.orm import Session
from app.modules.appointment.model import Appointment
from app.modules.appointment.schema import AppointmentCreate

def create_appointment_db(db: Session, appointment_data: AppointmentCreate):
    appointment = Appointment(
        patient_id=appointment_data.patient_id,
        doctor_id=appointment_data.doctor_id,
        appointment_date=appointment_data.appointment_date,
        status="Scheduled"
    )
    db.add(appointment)
    db.commit()
    db.refresh(appointment)
    return appointment

def get_appointments_by_doctor_and_patient_db(db: Session, doctor_id: int, patient_id: int):
    return db.query(Appointment).filter(
        Appointment.doctor_id == doctor_id,
        Appointment.patient_id == patient_id
    ).all()

def get_appointments_by_doctor_db(db: Session, doctor_id: int):
    return db.query(Appointment).filter(
        Appointment.doctor_id == doctor_id
    ).all()

def get_appointments_by_patient_db(db: Session, patient_id: int):
    return db.query(Appointment).filter(
        Appointment.patient_id == patient_id
    ).all()

def get_appointment_by_id_db(db: Session, appointment_id: int):
    return db.query(Appointment).filter(
        Appointment.appointment_id == appointment_id
    ).first()

def delete_appointment_db(db: Session, appointment_id: int):
    appointment = db.query(Appointment).filter(Appointment.appointment_id == appointment_id).first()
    if not appointment:
        return False
    db.delete(appointment)
    db.commit()
    return True