from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.rbac import require_role
from app.database.database import SessionLocal
from app.modules.user.model import User
from app.modules.appointment.model import Appointment

admin_router = APIRouter(
    prefix="/admin",
    tags=["Admin"],
    dependencies=[Depends(require_role(["Admin"]))]
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@admin_router.get("/users")
def list_all_users(db: Session = Depends(get_db)):
    return db.query(User).all()

@admin_router.get("/appointments")
def list_all_appointments(db: Session = Depends(get_db)):
    return db.query(Appointment).all() 