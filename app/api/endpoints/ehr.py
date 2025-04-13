from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.models.ehr_summary import EHRSummary
from app.models import EHR
from app.schemas import EHRSchema, EHRSummarySchema
from app.database.database import SessionLocal

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/")
def create_ehr(ehr: EHRSchema, db: Session = Depends(get_db)):
    new_ehr = EHR(**ehr.dict())
    db.add(new_ehr)
    db.commit()
    db.refresh(new_ehr)
    return {"message": "EHR added", "record_id": new_ehr.record_id}

@router.get("/{patient_id}")
def get_ehrs(patient_id: int, db: Session = Depends(get_db)):
    records = db.query(EHR).filter(EHR.patient_id == patient_id).all()
    if not records:
        raise HTTPException(status_code=404, detail="No EHR found")
    return {"records": records}

# ✅ Store EHR Summary
@router.post("/summaries/")
def store_ehr_summary(summary: EHRSummarySchema, db: Session = Depends(get_db)):
    new_summary = EHRSummary(**summary.dict())
    db.add(new_summary)
    db.commit()
    db.refresh(new_summary)
    return {"message": "EHR Summary saved", "summary_id": new_summary.id}

# ✅ Fetch EHR Summary
@router.get("/summaries/{patient_id}")
def get_ehr_summaries(patient_id: int, db: Session = Depends(get_db)):
    summaries = db.query(EHRSummary).filter(EHRSummary.user_id == patient_id).all()
    if not summaries:
        raise HTTPException(status_code=404, detail="No EHR summaries found")
    return {"ehr_summaries": summaries}