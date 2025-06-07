from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.modules.ehrsummary.schema import EHRSummarySchema
from app.database.database import get_db
from app.modules.user.deps import get_current_user
from app.modules.user.model import User
from app.rbac import require_role
from app.modules.ehrsummary.routes import (
    create_ehr_summary_db,
    get_ehr_summary_by_user_id_db,
    update_ehr_summary_db,
    delete_ehr_summary_db,
)

admin_ehr_summary_router = APIRouter(
    prefix="/ehrsummary",
    tags=["Admin EHR Summary"],
    dependencies=[Depends(require_role(["Admin"]))]
)

@admin_ehr_summary_router.post("/", response_model=EHRSummarySchema, status_code=status.HTTP_201_CREATED)
async def admin_create_ehr_summary(
    summary_data: EHRSummarySchema,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return create_ehr_summary_db(db, summary_data)

@admin_ehr_summary_router.get("/user/{user_id}", response_model=list[EHRSummarySchema])
async def admin_get_ehr_summaries_by_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    summaries = get_ehr_summary_by_user_id_db(db, user_id)
    if not summaries:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No EHR summaries found for this user.")
    return summaries

@admin_ehr_summary_router.put("/{summary_id}", response_model=EHRSummarySchema)
async def admin_update_ehr_summary(
    summary_id: int,
    summary_data: EHRSummarySchema,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    updated = update_ehr_summary_db(db, summary_id, summary_data)
    if not updated:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="EHR summary not found.")
    return updated

@admin_ehr_summary_router.delete("/{summary_id}", status_code=status.HTTP_204_NO_CONTENT)
async def admin_delete_ehr_summary(
    summary_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    success = delete_ehr_summary_db(db, summary_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="EHR summary not found.")
    return