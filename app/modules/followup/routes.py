from sqlalchemy.orm import Session
from app.modules.followup.model import FollowUp
from app.modules.followup.schema import FollowUpCreate

def create_followup_db(db: Session, followup_data: FollowUpCreate):
    followup = FollowUp(**followup_data.dict())
    db.add(followup)
    db.commit()
    db.refresh(followup)
    return followup

def get_followups_by_user_id_db(db: Session, user_id: int):
    return db.query(FollowUp).filter(FollowUp.user_id == user_id).all()

def get_followup_by_id_db(db: Session, followup_id: int):
    return db.query(FollowUp).filter(FollowUp.id == followup_id).first()

def update_followup_db(db: Session, followup_id: int, followup_data: FollowUpCreate):
    followup = db.query(FollowUp).filter(FollowUp.id == followup_id).first()
    if not followup:
        return None
    for field, value in followup_data.dict(exclude_unset=True).items():
        setattr(followup, field, value)
    db.commit()
    db.refresh(followup)
    return followup

def delete_followup_db(db: Session, followup_id: int):
    followup = db.query(FollowUp).filter(FollowUp.id == followup_id).first()
    if not followup:
        return False
    db.delete(followup)
    db.commit()
    return True