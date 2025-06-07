# app/modules/ehrsummary/routes.py

from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from app.modules.ehrsummary.model import EHRSummary
from app.modules.ehrsummary.schema import EHRSummarySchema
from app.database.database import get_db # Assuming get_db is in app.database.database

# Import User model and authentication dependencies for later use in role-specific modules
from app.modules.user.model import User # Assuming this is your User model
from app.modules.user.deps import get_current_user # Assuming this dependency exists
from app.rbac import require_role # Assuming this dependency exists
from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from app.modules.ehrsummary.model import EHRSummary
from app.modules.ehrsummary.schema import EHRSummarySchema
from app.database.database import get_db

# Import User model and authentication dependencies for later use in role-specific modules
from app.modules.user.model import User
from app.modules.user.deps import get_current_user
from app.rbac import require_role

router = APIRouter()

# --- Internal/Base CRUD Functions (could also be in a crud.py) ---
def create_ehr_summary_db(db: Session, summary_data: EHRSummarySchema) -> EHRSummary:
    new_summary = EHRSummary(**summary_data.dict())
    db.add(new_summary)
    db.commit()
    db.refresh(new_summary)
    return new_summary

def get_ehr_summary_by_user_id_db(db: Session, user_id: int) -> list[EHRSummary]:
    summaries = db.query(EHRSummary).filter(EHRSummary.user_id == user_id).all()
    return summaries

def update_ehr_summary_db(db: Session, summary_id: int, summary_data: EHRSummarySchema):
    summary = db.query(EHRSummary).filter(EHRSummary.id == summary_id).first()
    if not summary:
        return None
    for field, value in summary_data.dict(exclude_unset=True).items():
        setattr(summary, field, value)
    db.commit()
    db.refresh(summary)
    return summary

def delete_ehr_summary_db(db: Session, summary_id: int):
    summary = db.query(EHRSummary).filter(EHRSummary.id == summary_id).first()
    if not summary:
        return False
    db.delete(summary)
    db.commit()
    return True

# --- Base Endpoints (these will be included by role-specific routers) ---

@router.post("/", response_model=EHRSummarySchema, status_code=status.HTTP_201_CREATED)
def create_ehr_summary_base(summary: EHRSummarySchema, db: Session = Depends(get_db)):
    """
    Base endpoint to create an EHR summary. Access controlled by including routers.
    """
    return create_ehr_summary_db(db, summary)

@router.get("/{user_id}", response_model=list[EHRSummarySchema])
def get_ehr_summaries_base(user_id: int, db: Session = Depends(get_db)):
    """
    Base endpoint to get EHR summaries by user ID. Access controlled by including routers.
    """
    summaries = get_ehr_summary_by_user_id_db(db, user_id)
    if not summaries:
        return []
    return summaries
router = APIRouter()

# --- Internal/Base CRUD Functions (could also be in a crud.py) ---
def create_ehr_summary_db(db: Session, summary_data: EHRSummarySchema) -> EHRSummary:
    new_summary = EHRSummary(**summary_data.dict())
    db.add(new_summary)
    db.commit()
    db.refresh(new_summary)
    return new_summary

def get_ehr_summary_by_user_id_db(db: Session, user_id: int) -> list[EHRSummary]:
    summaries = db.query(EHRSummary).filter(EHRSummary.user_id == user_id).all()
    return summaries

# --- Base Endpoints (these will be included by role-specific routers) ---

# This endpoint handles the creation of an EHR summary.
# It will be protected by role-specific routers later.
@router.post("/", response_model=EHRSummarySchema, status_code=status.HTTP_201_CREATED)
def create_ehr_summary_base(summary: EHRSummarySchema, db: Session = Depends(get_db)):
    """
    Base endpoint to create an EHR summary. Access controlled by including routers.
    """
    return create_ehr_summary_db(db, summary)

# This endpoint retrieves EHR summaries for a specific user ID.
# It will be protected by role-specific routers later to ensure ownership/permissions.
@router.get("/{user_id}", response_model=list[EHRSummarySchema])
def get_ehr_summaries_base(user_id: int, db: Session = Depends(get_db)):
    """
    Base endpoint to get EHR summaries by user ID. Access controlled by including routers.
    """
    summaries = get_ehr_summary_by_user_id_db(db, user_id)
    if not summaries:
        # Returning 200 with empty list is generally preferred for collection endpoints
        # if no items are found for the queried criteria.
        return [] # Don't raise 404 here, let role-specific routers decide on 404/403 for access.
    return summaries

# TODO: Add PUT/PATCH for updating EHR summary
# TODO: Add DELETE for deleting EHR summary (likely admin-only)