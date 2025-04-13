from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.models import User
from app.schemas import UserSchema
from app.database.database import SessionLocal

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/")
def create_user(user: UserSchema, db: Session = Depends(get_db)):
    new_user = User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "User added", "user": user}