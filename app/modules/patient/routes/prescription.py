from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database.database import get_db
from app.modules.user.deps import get_current_patient
from app.modules.prescription.schema import PrescriptionResponse
from app.modules.prescription.routes import get_prescriptions_by_patient_id_db
from app.rbac import require_role

patient_prescription_router = APIRouter(
    prefix="/prescriptions",
    tags=["Patient Prescriptions"],
    dependencies=[Depends(require_role(["Patient"]))]
)

@patient_prescription_router.get("/", response_model=List[PrescriptionResponse])
def get_my_prescriptions(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_patient)
):
    return get_prescriptions_by_patient_id_db(db, current_user.user_id)