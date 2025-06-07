from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.modules.ehrsummary.schema import EHRSummarySchema
from app.database.database import get_db
from app.modules.user.deps import get_current_user
from app.modules.user.model import User
from app.rbac import require_role
from app.modules.ehrsummary.routes import get_ehr_summary_by_user_id_db
from app.modules.doctor.utils import has_appointment_with_patient

doctor_ehr_summary_router = APIRouter(
    prefix="/ehrsummary",
    tags=["Doctor EHR Summary"],
    dependencies=[Depends(require_role(["Doctor"]))]
)

@doctor_ehr_summary_router.get("/patient/{patient_id}", response_model=list[EHRSummarySchema])
async def get_patient_ehr_summaries(
    patient_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not has_appointment_with_patient(db, doctor_id=current_user.id, patient_id=patient_id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No appointment with this patient.")
    summaries = get_ehr_summary_by_user_id_db(db, patient_id)
    if not summaries:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No EHR summaries found for this patient.")
    return summaries