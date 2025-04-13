from sqlalchemy import Column, Integer, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from app.database.database import Base

class EHRSummary(Base):
    __tablename__ = 'ehr_summaries'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    ehr_data = Column(JSONB)
    updated_at = Column(DateTime)