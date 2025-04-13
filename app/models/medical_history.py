from sqlalchemy import Column, Integer, String, Date, ForeignKey
from app.database.database import Base

class MedicalHistory(Base):
    __tablename__ = 'medical_history'
    history_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    condition = Column(String)
    treatment = Column(String)
    start_date = Column(Date)
    end_date = Column(Date)