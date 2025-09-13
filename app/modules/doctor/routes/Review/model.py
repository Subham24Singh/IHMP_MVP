# # app/modules/review/model.py
# from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
# from sqlalchemy.orm import relationship
# from app.database.database import Base
# from datetime import datetime

# class Review(Base):
#     __tablename__ = "reviews"
#     review_id = Column(Integer, primary_key=True, index=True)
#     doctor_id = Column(Integer, ForeignKey("doctors.id", ondelete="CASCADE"), nullable=False)
#     patient_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False) # Or patients.id if separate
#     rating = Column(Integer, nullable=False) # 1 to 5
#     comment = Column(Text, nullable=True)
#     created_at = Column(DateTime, default=datetime.utcnow) # Store in UTC

#     doctor = relationship("Doctor", back_populates="reviews")
#     patient = relationship("User") # Assuming Patient is a User role