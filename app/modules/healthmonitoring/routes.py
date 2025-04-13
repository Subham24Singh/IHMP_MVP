from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.modules.healthmonitoring.model import HealthMonitoringLogs  # Ensure this matches the model file
from app.modules.healthmonitoring.schema import HealthMonitoringLogsSchema
from app.database.database import SessionLocal

router = APIRouter()

router = APIRouter()
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/")
def create_health_log(log: HealthMonitoringLogsSchema, db: Session = Depends(get_db)):
    new_log = HealthMonitoringLogs(**log.dict())
    db.add(new_log)
    db.commit()
    db.refresh(new_log)
    return {"message": "Health monitoring log created", "log_id": new_log.id}

@router.get("/{user_id}")
def get_health_logs(user_id: int, db: Session = Depends(get_db)):
    logs = db.query(HealthMonitoringLogs).filter(HealthMonitoringLogs.user_id == user_id).all()
    if not logs:
        raise HTTPException(status_code=404, detail="No health logs found")
    return {"health_logs": logs}