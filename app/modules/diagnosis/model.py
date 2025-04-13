from sqlalchemy import Column, Integer, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from app.database.database import Base

class DiagnosticInsights(Base):
    __tablename__ = 'diagnostic_insights'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    insights = Column(JSONB)
    generated_at = Column(DateTime)