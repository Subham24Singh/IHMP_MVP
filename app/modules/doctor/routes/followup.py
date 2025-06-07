from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database.database import get_db
from app.modules.doctor.deps import get_current_doctor
from app.modules.followup.schema import FollowUpResponse
from app.modules.followup.routes import get_followups_by_user_id_db
from app.modules.doctor.utils import has_appointment_with_patient
from app.rbac import require_role

doctor_follow_up_router = APIRouter(
    prefix="/followup",
    tags=["Doctor Follow-Up"],
    dependencies=[Depends(require_role(["Doctor"]))]
)

@doctor_follow_up_router.get("/patient/{patient_id}", response_model=List[FollowUpResponse])
def get_patient_followups(
    patient_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_doctor)
):
    if not has_appointment_with_patient(db, doctor_id=current_user.user_id, patient_id=patient_id):
        raise HTTPException(status_code=403, detail="No appointment with this patient.")
    return get_followups_by_user_id_db(db, patient_id)