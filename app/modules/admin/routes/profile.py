from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.modules.user.deps import get_current_user
from app.modules.Profile.schema import UserProfileResponse, UserProfileUpdate
from app.modules.Profile.routes import get_user_profile_db, update_user_profile_db

admin_profile_router = APIRouter(prefix="/profile", tags=["Profile"])

@admin_profile_router.get("/", response_model=UserProfileResponse)
def get_profile(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    user = get_user_profile_db(db, current_user.user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@admin_profile_router.put("/", response_model=UserProfileResponse)
def update_profile(
    profile_data: UserProfileUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    user = update_user_profile_db(db, current_user.user_id, profile_data)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user