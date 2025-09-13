from sqlalchemy import Column, Integer, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from app.database.base import Base

class FollowUp(Base):
    __tablename__ = 'followup_recommendations'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    recommendations = Column(JSONB, nullable=False)
    recommended_at = Column(DateTime, nullable=False)