from sqlalchemy.orm import Session
from app.modules.ehr.models import EHR
from app.modules.ehr.schema import EHRCreate 

def create_ehr_db(db: Session, ehr_data: EHRCreate):
    ehr = EHR(**ehr_data.dict())
    db.add(ehr)
    db.commit()
    db.refresh(ehr)
    return ehr

def get_ehrs_by_user_id_db(db: Session, user_id: int):
    return db.query(EHR).filter(EHR.user_id == user_id).all()

def get_ehr_by_id_db(db: Session, ehr_id: int):
    return db.query(EHR).filter(EHR.id == ehr_id).first()

def update_ehr_db(db: Session, ehr_id: int, ehr_data: EHRCreate):
    ehr = db.query(EHR).filter(EHR.id == ehr_id).first()
    if not ehr:
        return None
    for field, value in ehr_data.dict(exclude_unset=True).items():
        setattr(ehr, field, value)
    db.commit()
    db.refresh(ehr)
    return ehr

def delete_ehr_db(db: Session, ehr_id: int):
    ehr = db.query(EHR).filter(EHR.id == ehr_id).first()
    if not ehr:
        return False
    db.delete(ehr)
    db.commit()
    return True