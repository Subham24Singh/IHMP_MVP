from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.models.diagnostic_insights import DiagnosticInsights
from app.schemas.diagnostics_insights import DiagnosticInsightsSchema
from app.database.database import SessionLocal

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/")
def create_diagnostic_insight(insight: DiagnosticInsightsSchema, db: Session = Depends(get_db)):
    new_insight = DiagnosticInsights(**insight.dict())
    db.add(new_insight)
    db.commit()
    db.refresh(new_insight)
    return {"message": "Diagnostic Insight created", "insight_id": new_insight.id}

@router.get("/{patient_id}")
def get_diagnostic_insights(patient_id: int, db: Session = Depends(get_db)):
    insights = db.query(DiagnosticInsights).filter(DiagnosticInsights.user_id == patient_id).all()
    if not insights:
        raise HTTPException(status_code=404, detail="No diagnostic insights found")
    return {"diagnostic_insights": insights}
