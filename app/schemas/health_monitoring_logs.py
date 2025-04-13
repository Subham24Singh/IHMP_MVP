from pydantic import BaseModel
from datetime import datetime
from typing import Dict, Any

class HealthMonitoringLogsSchema(BaseModel):
    user_id: int
    monitoring_data: Dict[str, Any]
    logged_at: datetime = datetime.utcnow()

    class Config:
        orm_mode = True