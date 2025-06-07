from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database.database import get_db
from app.modules.doctor.deps import get_current_doctor
from app.modules.prescription.schema import PrescriptionCreate, PrescriptionResponse
from app.modules.prescription.routes import (
    create_prescription_db,
    get_prescriptions_by_doctor_id_db,
    get_prescriptions_by_patient_id_db,
    get_prescription_by_id_db,
    update_prescription_db,
    delete_prescription_db
)
from app.rbac import require_role

doctor_prescription_router = APIRouter(
    prefix="/prescriptions",
    tags=["Doctor Prescriptions"],
    dependencies=[Depends(require_role(["Doctor"]))]
)

@doctor_prescription_router.post("/", response_model=PrescriptionResponse)
def create_prescription(
    prescription_data: PrescriptionCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_doctor)
):
    # Only allow doctor to create for themselves
    if prescription_data.doctor_id != current_user.user_id:
        raise HTTPException(status_code=403, detail="You can only create prescriptions as yourself.")
    return create_prescription_db(db, prescription_data)

@doctor_prescription_router.get("/", response_model=List[PrescriptionResponse])
def get_my_prescriptions(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_doctor)
):
    return get_prescriptions_by_doctor_id_db(db, current_user.user_id)

@doctor_prescription_router.get("/patient/{patient_id}", response_model=List[PrescriptionResponse])
def get_patient_prescriptions(
    patient_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_doctor)
):
    # Optionally, check if doctor has appointment with patient
    return get_prescriptions_by_patient_id_db(db, patient_id)