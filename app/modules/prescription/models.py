from sqlalchemy import Column, Integer, String, ForeignKey
from app.database.database import Base

class Prescription(Base):
    __tablename__ = 'prescriptions'
    prescription_id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey('users.user_id'))
    doctor_id = Column(Integer, ForeignKey('users.user_id'))
    medication = Column(String)
    dosage = Column(String)