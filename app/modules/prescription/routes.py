from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.modules.user import  User
from app.modules.prescription.models import Prescription
from app.modules.prescription.schema import PrescriptionSchema
from app.database.database import SessionLocal
from app.database.database import get_db

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/")
def add_prescription(prescription: PrescriptionSchema, db: Session = Depends(get_db)):
    # Check if patient exists
    patient = db.query(User).filter(User.user_id == prescription.patient_id, User.role == "Patient").first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    # Check if doctor exists
    doctor = db.query(User).filter(User.user_id == prescription.doctor_id, User.role == "Doctor").first()
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")

    new_prescription = Prescription(**prescription.dict())
    db.add(new_prescription)
    db.commit()
    db.refresh(new_prescription)
    return {"message": "Prescription added", "prescription_id": new_prescription.prescription_id}

@router.get("/{patient_id}")
def get_prescriptions(patient_id: int, db: Session = Depends(get_db)):
    prescriptions = db.query(Prescription).filter(Prescription.patient_id == patient_id).all()
    if not prescriptions:
        raise HTTPException(status_code=404, detail="No prescriptions found")
    return {"prescriptions": prescriptions}