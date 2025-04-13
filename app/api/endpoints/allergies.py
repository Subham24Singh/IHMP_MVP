from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.models import AllergyTracking, User
from app.schemas import AllergyTrackingCreate
from app.database.database import SessionLocal

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/")
def create_allergy(allergy_data: AllergyTrackingCreate, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.user_id == allergy_data.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    allergy = AllergyTracking(**allergy_data.dict())
    db.add(allergy)
    db.commit()
    db.refresh(allergy)
    return {"message": "Allergy added", "allergy_id": allergy.allergy_id}

@router.get("/{user_id}")
def get_allergies(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.user_id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    allergies = db.query(AllergyTracking).filter(AllergyTracking.user_id == user_id).all()
    if not allergies:
        raise HTTPException(status_code=404, detail="No allergies found for this user")
    
    return {"user_id": user_id, "allergies": allergies}