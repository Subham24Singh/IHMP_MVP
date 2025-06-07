from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database.database import get_db
from app.modules.doctor.deps import get_current_doctor
from app.modules.ehr.schema import EHRResponse
from app.modules.ehr.routes import get_ehrs_by_user_id_db, get_ehr_by_id_db
from app.modules.doctor.utils import has_appointment_with_patient
from app.rbac import require_role

doctor_ehr_router = APIRouter(
    prefix="/ehr",
    tags=["Doctor EHR"],
    dependencies=[Depends(require_role(["Doctor"]))]
)

@doctor_ehr_router.get("/patient/{patient_id}", response_model=List[EHRResponse])
def get_patient_ehrs(
    patient_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_doctor)
):
    # Only allow if doctor has an appointment with the patient
    if not has_appointment_with_patient(db, doctor_id=current_user.user_id, patient_id=patient_id):
        raise HTTPException(status_code=403, detail="No appointment with this patient.")
    return get_ehrs_by_user_id_db(db, patient_id)