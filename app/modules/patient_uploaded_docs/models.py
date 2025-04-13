from sqlalchemy import Column, Integer, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from app.database.database import Base

class PatientUploadedDocs(Base):
    __tablename__ = 'patient_uploaded_docs'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    document_data = Column(JSONB)
    uploaded_at = Column(DateTime)