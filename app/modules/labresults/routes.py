from sqlalchemy.orm import Session
from app.modules.labresults.model import LabResults
from app.modules.labresults.schema import LabResultCreate

def create_lab_result_db(db: Session, lab_result_data: LabResultCreate):
    lab_result = LabResults(**lab_result_data.dict())
    db.add(lab_result)
    db.commit()
    db.refresh(lab_result)
    return lab_result

def get_lab_results_by_user_id_db(db: Session, user_id: int):
    return db.query(LabResults).filter(LabResults.user_id == user_id).all()

def get_lab_result_by_id_db(db: Session, lab_result_id: int):
    return db.query(LabResults).filter(LabResults.id == lab_result_id).first()



def update_lab_result_db(db: Session, lab_result_id: int, lab_result_data: LabResultCreate):
    lab_result = db.query(LabResults).filter(LabResults.id == lab_result_id).first()
    if not lab_result:
        return None
    for field, value in lab_result_data.dict(exclude_unset=True).items():
        setattr(lab_result, field, value)
    db.commit()
    db.refresh(lab_result)
    return lab_result

def delete_lab_result_db(db: Session, lab_result_id: int):
    lab_result = db.query(LabResults).filter(LabResults.id == lab_result_id).first()
    if not lab_result:
        return False
    db.delete(lab_result)
    db.commit()
    return True