from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from app.database.database import Base

class Doctor(Base):
    __tablename__ = 'doctors'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, nullable=True)
