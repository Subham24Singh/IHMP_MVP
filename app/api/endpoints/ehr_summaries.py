from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.models.ehr_summary import EHRSummary
from app.schemas.ehr_summaries import EHRSummarySchema
from app.database.database import SessionLocal

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/")
def create_ehr_summary(summary: EHRSummarySchema, db: Session = Depends(get_db)):
    new_summary = EHRSummary(**summary.dict())
    db.add(new_summary)
    db.commit()
    db.refresh(new_summary)
    return {"message": "EHR Summary created", "summary_id": new_summary.id}

@router.get("/{user_id}")
def get_ehr_summaries(user_id: int, db: Session = Depends(get_db)):
    summaries = db.query(EHRSummary).filter(EHRSummary.user_id == user_id).all()
    if not summaries:
        raise HTTPException(status_code=404, detail="No EHR summaries found")
    return {"ehr_summaries": summaries}