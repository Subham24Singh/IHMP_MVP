from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.modules.doctor.deps import get_current_doctor, verify_doctor_patient_link
from app.modules.healthmonitoring.model import HealthMonitoringLogs
from app.modules.user.model import User
from app.rbac import require_role

router = APIRouter(dependencies=[Depends(require_role(["Doctor"]))])

@router.get("/{patient_id}")
def get_health_logs_for_patient(
    patient_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_doctor)
):
    # 👇 Verify doctor-patient relationship
    verify_doctor_patient_link(current_user.user_id, patient_id, db)

    logs = db.query(HealthMonitoringLogs).filter_by(user_id=patient_id).all()
    return logs
