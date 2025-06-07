from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.modules.medical_history.models import MedicalHistory
from app.modules.medical_history.schema import MedicalHistorySchema
from app.database.database import SessionLocal
from app.rbac import require_role
from app.modules.user.deps import get_current_user
from app.modules.user.model import User

router = APIRouter(dependencies=[Depends(require_role(["Patient"]))])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/")
def add_medical_history(history: MedicalHistorySchema, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    # Only allow adding medical history for the current user
    if history.user_id != current_user.user_id:
        raise HTTPException(status_code=403, detail="Forbidden: Cannot add medical history for another user")
    new_history = MedicalHistory(**history.dict())
    db.add(new_history)
    db.commit()
    db.refresh(new_history)
    return {"message": "Medical history added", "history_id": new_history.history_id}

@router.get("/{user_id}")
def get_medical_history(user_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    # Only allow viewing medical history for the current user
    if user_id != current_user.user_id:
        raise HTTPException(status_code=403, detail="Forbidden: Cannot view medical history for another user")
    history = db.query(MedicalHistory).filter(MedicalHistory.user_id == user_id).all()
    if not history:
        raise HTTPException(status_code=404, detail="No medical history found")
    return {"history": history}