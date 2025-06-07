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
)

patient_ehr_summary_router = APIRouter(
    prefix="/ehrsummary",
    tags=["Patient EHR Summary"],
    dependencies=[Depends(require_role(["Patient"]))]
)

@patient_ehr_summary_router.post("/", response_model=EHRSummarySchema, status_code=status.HTTP_201_CREATED)
async def create_my_ehr_summary(
    summary_data: EHRSummarySchema,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if summary_data.user_id != current_user.user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You can only create your own EHR summary.")
    return create_ehr_summary_db(db, summary_data)

@patient_ehr_summary_router.get("/", response_model=list[EHRSummarySchema])
async def get_my_ehr_summaries(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    summaries = get_ehr_summary_by_user_id_db(db, current_user.user_id)
    if not summaries:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No EHR summaries found.")
    return summaries

@patient_ehr_summary_router.put("/{summary_id}", response_model=EHRSummarySchema)
async def update_my_ehr_summary(
    summary_id: int,
    summary_data: EHRSummarySchema,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if summary_data.user_id != current_user.user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You can only update your own EHR summary.")
    updated = update_ehr_summary_db(db, summary_id, summary_data)
    if not updated or updated.user_id != current_user.user_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="EHR summary not found.")
    return updated