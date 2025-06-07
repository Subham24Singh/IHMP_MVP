from sqlalchemy.orm import Session
from app.modules.prescription.models import Prescription
from app.modules.prescription.schema import PrescriptionCreate

def create_prescription_db(db: Session, prescription_data: PrescriptionCreate):
    prescription = Prescription(**prescription_data.dict())
    db.add(prescription)
    db.commit()
    db.refresh(prescription)
    return prescription

def get_prescriptions_by_patient_id_db(db: Session, patient_id: int):
    return db.query(Prescription).filter(Prescription.patient_id == patient_id).all()

def get_prescriptions_by_doctor_id_db(db: Session, doctor_id: int):
    return db.query(Prescription).filter(Prescription.doctor_id == doctor_id).all()

def get_prescription_by_id_db(db: Session, prescription_id: int):
    return db.query(Prescription).filter(Prescription.prescription_id == prescription_id).first()

def update_prescription_db(db: Session, prescription_id: int, prescription_data: PrescriptionCreate):
    prescription = db.query(Prescription).filter(Prescription.prescription_id == prescription_id).first()
    if not prescription:
        return None
    for field, value in prescription_data.dict(exclude_unset=True).items():
        setattr(prescription, field, value)
    db.commit()
    db.refresh(prescription)
    return prescription

def delete_prescription_db(db: Session, prescription_id: int):
    prescription = db.query(Prescription).filter(Prescription.prescription_id == prescription_id).first()
    if not prescription:
        return False
    db.delete(prescription)
    db.commit()
    return True