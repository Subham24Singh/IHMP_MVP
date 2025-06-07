from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database.database import get_db
from app.modules.user.deps import get_current_user
from app.modules.followup.schema import FollowUpCreate, FollowUpResponse
from app.modules.followup.routes import (
    create_followup_db,
    get_followups_by_user_id_db,
    get_followup_by_id_db,
    update_followup_db,
    delete_followup_db
)
from app.rbac import require_role

admin_follow_up_router = APIRouter(
    prefix="/followup",
    tags=["Admin Follow-Up"],
    dependencies=[Depends(require_role(["Admin"]))]
)

@admin_follow_up_router.post("/", response_model=FollowUpResponse)
def admin_create_followup(
    followup_data: FollowUpCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return create_followup_db(db, followup_data)

@admin_follow_up_router.get("/user/{user_id}", response_model=List[FollowUpResponse])
def admin_get_followups_by_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return get_followups_by_user_id_db(db, user_id)

@admin_follow_up_router.put("/{followup_id}", response_model=FollowUpResponse)
def admin_update_followup(
    followup_id: int,
    followup_data: FollowUpCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    updated = update_followup_db(db, followup_id, followup_data)
    if not updated:
        raise HTTPException(status_code=404, detail="Follow-up not found.")
    return updated

@admin_follow_up_router.delete("/{followup_id}", status_code=204)
def admin_delete_followup(
    followup_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    success = delete_followup_db(db, followup_id)
    if not success:
        raise HTTPException(status_code=404, detail="Follow-up not found.")
    return