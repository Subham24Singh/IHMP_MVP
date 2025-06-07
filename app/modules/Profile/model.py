from sqlalchemy import Column, Integer, String, Date, Enum
from app.database.database import Base

class User(Base):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    phone_number = Column(String)
    date_of_birth = Column(String)
    role = Column(String, nullable=False)
    blood_type = Column(String)
    emergency_contact = Column(String)
    # Add more fields as needed