from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database.database import get_db
from app.modules.user.deps import get_current_patient
from app.modules.followup.schema import FollowUpCreate, FollowUpResponse
from app.modules.followup.routes import (
    create_followup_db,
    get_followups_by_user_id_db,
    get_followup_by_id_db,
    update_followup_db,
    delete_followup_db
)
from app.rbac import require_role

patient_follow_up_router = APIRouter(
    prefix="/followup",
    tags=["Patient Follow-Up"],
    dependencies=[Depends(require_role(["Patient"]))]
)

@patient_follow_up_router.post("/", response_model=FollowUpResponse)
def create_followup(
    followup_data: FollowUpCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_patient)
):
    if followup_data.user_id != current_user.user_id:
        raise HTTPException(status_code=403, detail="You can only create your own follow-ups.")
    return create_followup_db(db, followup_data)

@patient_follow_up_router.get("/", response_model=List[FollowUpResponse])
def get_my_followups(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_patient)
):
    return get_followups_by_user_id_db(db, current_user.user_id)