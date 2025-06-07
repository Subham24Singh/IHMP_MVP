from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.modules.doctor.deps import get_current_doctor
from app.modules.Profile.schema import UserProfileResponse, UserProfileUpdate
from app.modules.Profile.routes import get_user_profile_db, update_user_profile_db

doctor_profile_router = APIRouter(prefix="/profile", tags=["Profile"])

@doctor_profile_router.get("/", response_model=UserProfileResponse)
def get_profile(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_doctor)
):
    user = get_user_profile_db(db, current_user.user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@doctor_profile_router.put("/", response_model=UserProfileResponse)
def update_profile(
    profile_data: UserProfileUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_doctor)
):
    user = update_user_profile_db(db, current_user.user_id, profile_data)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user