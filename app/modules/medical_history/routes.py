from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.modules.medical_history.models import MedicalHistory
from app.modules.medical_history.schema import MedicalHistorySchema
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
def add_medical_history(history: MedicalHistorySchema, db: Session = Depends(get_db)):
    new_history = MedicalHistory(**history.dict())
    db.add(new_history)
    db.commit()
    db.refresh(new_history)
    return {"message": "Medical history added", "history_id": new_history.history_id}

@router.get("/{user_id}")
def get_medical_history(user_id: int, db: Session = Depends(get_db)):
    history = db.query(MedicalHistory).filter(MedicalHistory.user_id == user_id).all()
    if not history:
        raise HTTPException(status_code=404, detail="No medical history found")
    return {"history": history}