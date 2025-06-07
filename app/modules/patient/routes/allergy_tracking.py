from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database.database import get_db
from app.modules.user.deps import get_current_patient
from app.modules.allergytracking.schema import AllergyTrackingCreate, AllergyTrackingResponse
from app.modules.allergytracking.routes import (
    create_allergy_tracking_db,
    get_allergies_by_user_id_db,
    get_allergy_by_id_db
)
from app.rbac import require_role

patient_allergy_tracking_router = APIRouter(
    prefix="/allergy_tracking",
    tags=["Patient Allergy Tracking"],
    dependencies=[Depends(require_role(["Patient"]))]
)

@patient_allergy_tracking_router.post("/", response_model=AllergyTrackingResponse)
def create_allergy(
    allergy_data: AllergyTrackingCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_patient)
):
    if allergy_data.user_id != current_user.user_id:
        raise HTTPException(status_code=403, detail="You can only create your own allergy records.")
    return create_allergy_tracking_db(db, allergy_data)

@patient_allergy_tracking_router.get("/", response_model=List[AllergyTrackingResponse])
def get_my_allergies(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_patient)
):
    return get_allergies_by_user_id_db(db, current_user.user_id)