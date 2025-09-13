# # app/modules/doctor/schema.py
# from pydantic import BaseModel, Field
# from datetime import datetime
# from typing import Optional, List

# # Assuming you have a Review schema if you implement reviews
# class ReviewBase(BaseModel):
#     patient_id: int
#     rating: int = Field(..., ge=1, le=5)
#     comment: Optional[str] = None
#     created_at: datetime

# class ReviewResponse(ReviewBase):
#     review_id: int
#     # You might want to include patient's name here for display
#     # patient_name: str

#     class Config:
#         from_attributes = True

# # Schema for listing doctors (less detail)
# class DoctorListItem(BaseModel):
#     id: int
#     full_name: str
#     specialty: str
#     clinic_address: str
#     education: Optional[str] = None
#     experience: Optional[int] = None
#     bio: Optional[str] = None
#     photo_url: Optional[str] = None
#     average_rating: float = 0.0 # From model
#     total_reviews: int = 0 # From model

#     class Config:
#         from_attributes = True

# # Schema for full doctor profile (when viewing details)
# class DoctorProfileResponse(BaseModel):
#     id: int
#     full_name: str
#     specialty: str
#     clinic_address: str
#     education: Optional[str] = None
#     experience: Optional[int] = None
#     bio: Optional[str] = None
#     photo_url: Optional[str] = None

#     # --- New Fields from Model ---
#     average_rating: float = 0.0
#     total_reviews: int = 0
#     # reviews: List[ReviewResponse] = [] # Include actual reviews if desired
#     working_hours: Optional[str] = None
#     next_available_slot: Optional[datetime] = None # Calculated in backend
#     certifications: Optional[str] = None
#     languages_spoken: Optional[List[str]] = None
#     fees: Optional[float] = None
#     insurance_accepted: Optional[bool] = False
#     areas_of_expertise: Optional[str] = None

#     class Config:
#         from_attributes = True # orm_mode for Pydantic v1