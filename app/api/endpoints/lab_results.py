from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.models import LabResults
from app.schemas import LabResultSchema
from app.database.database import SessionLocal

router = APIRouter()

router = APIRouter()
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/")
def add_lab_result(lab_result: LabResultSchema, db: Session = Depends(get_db)):
    new_result = LabResults(**lab_result.dict())
    db.add(new_result)
    db.commit()
    db.refresh(new_result)
    return {"message": "Lab result added", "result_id": new_result.result_id}

@router.get("/{user_id}")
def get_lab_results(user_id: int, db: Session = Depends(get_db)):
    results = db.query(LabResults).filter(LabResults.user_id == user_id).all()
    if not results:
        raise HTTPException(status_code=404, detail="No lab results found")
    return {"results": results}