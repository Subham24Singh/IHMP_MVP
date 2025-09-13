from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.modules.doctor.models import Doctor
from app.modules.doctor.routes.schema import DoctorProfileResponse
from app.modules.doctor.deps import get_current_doctor
from pydantic import BaseModel

router = APIRouter(prefix="/api/doctors", tags=["Doctors"])

class DoctorProfileUpdate(BaseModel):
    full_name: str
    specialty: str
    bio: str = ""
    education: str = ""
    experience: str = ""
    clinic_address: str
    photo_url: str = ""
    available_days: list[str] = []
    time_slots: str = ""

@router.get("/{doctor_id}/profile", response_model=DoctorProfileResponse)
def get_doctor_profile(
    doctor_id: int,
    db: Session = Depends(get_db)
):
    """Get a doctor's profile details."""
    doctor = db.query(Doctor).filter(Doctor.id == doctor_id).first()
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    return doctor

@router.post("/update-profile")
def update_profile(
    profile: DoctorProfileUpdate,
    db: Session = Depends(get_db),
    current_doctor=Depends(get_current_doctor)
):
    doctor = db.query(Doctor).filter(Doctor.id == current_doctor.user_id).first()
    if not doctor:
        doctor = Doctor(id=current_doctor.user_id)
        db.add(doctor)
    
    # Update doctor's profile
    for field, value in profile.dict().items():
        setattr(doctor, field, value)
    
    db.commit()
    db.refresh(doctor)
    return {"success": True, "doctor": DoctorProfileResponse.from_orm(doctor)}