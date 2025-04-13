from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from app.database.database import Base

class Recovery(Base):
    __tablename__ = 'recoverys'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, nullable=True)
