from sqlalchemy import Column, Integer, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from app.database.database import Base

class HealthMonitoringLogs(Base):
    __tablename__ = 'health_monitoring_logs'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    monitoring_data = Column(JSONB)
    logged_at = Column(DateTime)