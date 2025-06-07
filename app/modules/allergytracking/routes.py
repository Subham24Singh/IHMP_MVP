from sqlalchemy.orm import Session
from app.modules.allergytracking.models import AllergyTracking
from app.modules.allergytracking.schema import AllergyTrackingCreate

def create_allergy_tracking_db(db: Session, allergy_data: AllergyTrackingCreate):
    allergy = AllergyTracking(**allergy_data.dict())
    db.add(allergy)
    db.commit()
    db.refresh(allergy)
    return allergy

def get_allergies_by_user_id_db(db: Session, user_id: int):
    return db.query(AllergyTracking).filter(AllergyTracking.user_id == user_id).all()

def get_allergy_by_id_db(db: Session, allergy_id: int):
    return db.query(AllergyTracking).filter(AllergyTracking.id == allergy_id).first()