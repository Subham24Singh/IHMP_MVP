from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database.database import get_db
from app.modules.user.deps import get_current_patient
from app.modules.labresults.schema import LabResultCreate, LabResultResponse
from app.modules.labresults.routes import (
    create_lab_result_db,
    get_lab_results_by_user_id_db,
    get_lab_result_by_id_db
)
from app.rbac import require_role

patient_lab_results_router = APIRouter(
    prefix="/labresults",
    tags=["Patient Lab Results"],
    dependencies=[Depends(require_role(["Patient"]))]
)

@patient_lab_results_router.post("/", response_model=LabResultResponse)
def create_lab_result(
    lab_result_data: LabResultCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_patient)
):
    if lab_result_data.user_id != current_user.user_id:
        raise HTTPException(status_code=403, detail="You can only create your own lab results.")
    return create_lab_result_db(db, lab_result_data)

@patient_lab_results_router.get("/", response_model=List[LabResultResponse])
def get_my_lab_results(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_patient)
):
    return get_lab_results_by_user_id_db(db, current_user.user_id)