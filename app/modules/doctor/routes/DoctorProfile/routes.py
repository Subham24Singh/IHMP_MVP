# from fastapi import APIRouter, Depends, HTTPException, status
# from sqlalchemy.orm import Session, joinedload # Import joinedload for eager loading
# from typing import List, Optional
# from datetime import datetime, timedelta, timezone
# import pytz # for timezone handling
# import logging

# from app.database.database import get_db
# # Ensure you import your Doctor model correctly
# from app.modules.doctor.routes.model import Doctor # Assuming Doctor model is here
# from app.modules.user.model import User # Assuming User model is here for linking

# # Import the new schemas
# from app.modules.doctor.routes.schema import DoctorListItem, DoctorProfileResponse, ReviewResponse
# # Assuming you have a Review model in app/modules/review/model.py
# from app.modules.doctor.routes.Review.model import Review # You'd need to create this model

# router = APIRouter(prefix="/doctors", tags=["Doctors"]) # Renamed prefix to /doctors for clarity

# # Configuration for timezone (same as in your patient appointments)
# from app.config import settings
# def get_current_timezone_aware_time():
#     tz = pytz.timezone(settings.TIMEZONE)
#     return datetime.now(tz)

# @router.get("/", response_model=List[DoctorListItem])
# def get_all_doctors(db: Session = Depends(get_db)):
#     """
#     Retrieves a list of all doctors with essential details for listing.
#     """
#     # Eager load relationships if needed for list view (e.g., average_rating calculation)
#     doctors = db.query(Doctor).all()
#     # No 404 for empty list; return empty list for better UX
#     return doctors

# @router.get("/{doctor_id}", response_model=DoctorProfileResponse)
# def get_doctor_details(doctor_id: int, db: Session = Depends(get_db)):
#     """
#     Retrieves the full profile details for a specific doctor.
#     Includes calculated next available slot and associated reviews.
#     """
#     # Eager load reviews if you want them in the response model, otherwise fetch separately
#     doctor = db.query(Doctor).options(joinedload(Doctor.reviews)).filter(Doctor.id == doctor_id).first()
#     if not doctor:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Doctor not found")

#     # --- Simulate Next Available Slot (Dynamic Feature) ---
#     # In a real app, this would involve complex logic looking at:
#     # 1. Doctor's defined working hours (e.g., from a 'DoctorAvailability' table)
#     # 2. Existing booked appointments for that doctor
#     # 3. Appointment duration (e.g., 30 minutes per appointment)

#     # For now, a simplified example: find first available slot 30 mins after current time
#     now_aware = get_current_timezone_aware_time()
#     next_30_mins = now_aware + timedelta(minutes=30)
#     # Convert to UTC if your DB stores appointments in UTC
#     next_30_mins_utc = next_30_mins.astimezone(timezone.utc) if next_30_mins.tzinfo else next_30_mins.replace(tzinfo=timezone.utc)

#     # Fetch existing appointments for the doctor from now onwards
#     from app.modules.appointment.model import Appointment # Ensure Appointment model is imported
#     upcoming_appointments = db.query(Appointment).filter(
#         Appointment.doctor_id == doctor.id,
#         Appointment.appointment_date >= next_30_mins_utc.date(), # Start from today/future
#         Appointment.status.in_(["Scheduled", "Confirmed"])
#     ).order_by(Appointment.appointment_date).all()

#     # Simple logic to find the next available slot (VERY BASIC)
#     # A real system would iterate through working hours slots and check against bookings.
#     simulated_next_available_slot = None
#     candidate_slot = next_30_mins.replace(second=0, microsecond=0) # Round to nearest minute for simplicity

#     # Find the next whole 30-minute slot
#     if candidate_slot.minute < 30:
#         candidate_slot = candidate_slot.replace(minute=30)
#     else:
#         candidate_slot = candidate_slot.replace(minute=0, hour=candidate_slot.hour + 1)

#     # This is a placeholder. A robust system checks actual availability blocks.
#     # For demonstration, let's assume the first available 30-min slot is 1 hour from now.
#     simulated_next_available_slot = now_aware + timedelta(hours=1)
#     simulated_next_available_slot = simulated_next_available_slot.replace(second=0, microsecond=0)


#     # --- Real-Time Rating Visibility ---
#     # This is handled by including `average_rating` and `total_reviews` directly
#     # in the `DoctorProfileResponse` schema and populating them from the `Doctor` model.
#     # The `average_rating` and `total_reviews` columns in the Doctor model
#     # would need to be updated whenever a new review is submitted or an existing one changes.

#     # Example of how to calculate on the fly (less performant for many requests,
#     # but demonstrates the concept if you haven't pre-calculated)
#     # reviews_for_doctor = db.query(Review).filter(Review.doctor_id == doctor.id).all()
#     # if reviews_for_doctor:
#     #     doctor.average_rating = sum(r.rating for r in reviews_for_doctor) / len(reviews_for_doctor)
#     #     doctor.total_reviews = len(reviews_for_doctor)
#     # else:
#     #     doctor.average_rating = 0.0
#     #     doctor.total_reviews = 0


#     # If you want to return actual reviews in the profile, you'd add:
#     # reviews_data = [ReviewResponse.from_orm(r) for r in doctor.reviews]

#     # Create the response dictionary, including the simulated next_available_slot
#     response_data = {
#         "id": doctor.id,
#         "full_name": doctor.full_name,
#         "specialty": doctor.specialty,
#         "clinic_address": doctor.clinic_address,
#         "education": doctor.education,
#         "experience": doctor.experience,
#         "bio": doctor.bio,
#         "photo_url": doctor.photo_url,
#         "average_rating": doctor.average_rating,
#         "total_reviews": doctor.total_reviews,
#         "working_hours": doctor.working_hours, # From model
#         "next_available_slot": simulated_next_available_slot, # Calculated
#         "certifications": doctor.certifications,
#         "languages_spoken": doctor.languages_spoken,
#         "fees": doctor.fees,
#         "insurance_accepted": doctor.insurance_accepted,
#         "areas_of_expertise": doctor.areas_of_expertise,
#         # "reviews": reviews_data # Uncomment if including reviews in profile response
#     }
#     return response_data