from sqlalchemy.orm import Session
from app.modules.appointment.model import Appointment  # adjust import as needed

def has_appointment_with_patient(db: Session, doctor_id: int, patient_id: int) -> bool:
    """
    Returns True if the doctor has at least one appointment with the patient.
    """
    return db.query(Appointment).filter_by(doctor_id=doctor_id, patient_id=patient_id).first() is not None