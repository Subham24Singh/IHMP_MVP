from sqlalchemy import Column, Integer, String
from sqlalchemy import Column, Date, Integer, String, DateTime, Enum, ForeignKey, Text
from app.database.database import Base

class EHR(Base):
     __tablename__ = 'ehr'
     record_id = Column(Integer, primary_key=True, index=True)
     patient_id = Column(Integer, ForeignKey('users.user_id', ondelete="CASCADE"), nullable=False)
     diagnosis = Column(Text, nullable=False)
     treatment = Column(Text, nullable=False)
     notes = Column(Text)