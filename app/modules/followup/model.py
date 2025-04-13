from sqlalchemy import Column, Integer, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from app.database.database import Base

class FollowupRecommendations(Base):
    __tablename__ = 'followup_recommendations'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    recommendations = Column(JSONB)
    recommended_at = Column(DateTime)