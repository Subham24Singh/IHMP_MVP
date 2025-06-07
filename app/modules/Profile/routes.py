from sqlalchemy.orm import Session
from app.modules.user.model import User
from app.modules.Profile.schema import UserProfileUpdate

def get_user_profile_db(db: Session, user_id: int):
    return db.query(User).filter(User.user_id == user_id).first()

def update_user_profile_db(db: Session, user_id: int, profile_data: UserProfileUpdate):
    user = db.query(User).filter(User.user_id == user_id).first()
    if not user:
        return None
    for field, value in profile_data.dict(exclude_unset=True).items():
        setattr(user, field, value)
    db.commit()
    db.refresh(user)
    return user