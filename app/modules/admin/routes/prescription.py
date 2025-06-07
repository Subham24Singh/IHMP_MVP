from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database.database import get_db
from app.modules.user.deps import get_current_user
from app.modules.prescription.schema import PrescriptionCreate, PrescriptionResponse
from app.modules.prescription.routes import (
    create_prescription_db,
    get_prescriptions_by_patient_id_db,
    get_prescriptions_by_doctor_id_db,
    get_prescription_by_id_db,
    update_prescription_db,
    delete_prescription_db
)
from app.rbac import require_role

admin_prescription_router = APIRouter(
    prefix="/prescriptions",
    tags=["Admin Prescriptions"],
    dependencies=[Depends(require_role(["Admin"]))]
)

@admin_prescription_router.get("/patient/{patient_id}", response_model=List[PrescriptionResponse])
def get_patient_prescriptions(
    patient_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return get_prescriptions_by_patient_id_db(db, patient_id)

@admin_prescription_router.get("/doctor/{doctor_id}", response_model=List[PrescriptionResponse])
def get_doctor_prescriptions(
    doctor_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return get_prescriptions_by_doctor_id_db(db, doctor_id)

@admin_prescription_router.post("/", response_model=PrescriptionResponse)
def create_prescription(
    prescription_data: PrescriptionCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return create_prescription_db(db, prescription_data)

@admin_prescription_router.put("/{prescription_id}", response_model=PrescriptionResponse)
def update_prescription(
    prescription_id: int,
    prescription_data: PrescriptionCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    updated = update_prescription_db(db, prescription_id, prescription_data)
    if not updated:
        raise HTTPException(status_code=404, detail="Prescription not found.")
    return updated

@admin_prescription_router.delete("/{prescription_id}", status_code=204)
def delete_prescription(
    prescription_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    success = delete_prescription_db(db, prescription_id)
    if not success:
        raise HTTPException(status_code=404, detail="Prescription not found.")
    return