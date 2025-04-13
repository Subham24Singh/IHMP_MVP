from sqlalchemy import Column, Integer, String, ForeignKey
from app.database.database import Base

class LabResults(Base):
    __tablename__ = 'lab_results'
    result_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    test_name = Column(String)
    result_data = Column(String)