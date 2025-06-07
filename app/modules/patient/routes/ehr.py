from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database.database import get_db
from app.modules.user.deps import get_current_patient
from app.modules.ehr.schema import EHRCreate, EHRResponse
from app.modules.ehr.routes import (
    create_ehr_db,
    get_ehrs_by_user_id_db,
    get_ehr_by_id_db,
    update_ehr_db,
    delete_ehr_db
)
from app.rbac import require_role

patient_ehr_router = APIRouter(
    prefix="/ehr",
    tags=["Patient EHR"],
    dependencies=[Depends(require_role(["Patient"]))]
)

@patient_ehr_router.post("/", response_model=EHRResponse)
def create_ehr(
    ehr_data: EHRCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_patient)
):
    if ehr_data.user_id != current_user.user_id:
        raise HTTPException(status_code=403, detail="You can only create your own EHR.")
    return create_ehr_db(db, ehr_data)

@patient_ehr_router.get("/", response_model=List[EHRResponse])
def get_my_ehrs(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_patient)
):
    return get_ehrs_by_user_id_db(db, current_user.user_id)