from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database.database import Base

class AllergyTracking(Base):
    __tablename__ = 'allergy_tracking'
    allergy_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    allergy_name = Column(String)
    reaction = Column(String)
    user = relationship("User", back_populates="allergies")