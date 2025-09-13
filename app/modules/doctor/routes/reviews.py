from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from app.database.database import get_db
from app.modules.doctor.models import Review, Doctor
from app.modules.user.model import User
from app.modules.appointment.model import Appointment
from app.modules.user.deps import get_current_user

router = APIRouter(prefix="/api/reviews", tags=["Reviews"])

# POST /reviews
@router.post("/", response_model=dict)
def submit_review(
    review_data: dict,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # Ensure the user is not a doctor
    if current_user.role == "Doctor":
        raise HTTPException(status_code=403, detail="Doctors cannot post reviews")

    # Check if the user has had an appointment with the doctor
    appointment = db.query(Appointment).filter(
        Appointment.doctor_id == review_data["doctor_id"],
        Appointment.patient_id == current_user.user_id,
        Appointment.status == "Completed"
    ).first()

    if not appointment:
        raise HTTPException(
            status_code=403,
            detail="You can only review a doctor after completing an appointment with them."
        )

    # Create the review
    new_review = Review(
        doctor_id=review_data["doctor_id"],
        patient_id=current_user.user_id,
        rating=review_data["rating"],
        review_text=review_data.get("review_text"),
        review_date=datetime.utcnow(),
    )
    db.add(new_review)

    # Update doctor's average rating and total reviews
    reviews = db.query(Review).filter(Review.doctor_id == review_data["doctor_id"]).all()
    total_reviews = len(reviews)
    average_rating = sum([review.rating for review in reviews]) / total_reviews
    doctor = db.query(Doctor).filter(Doctor.id == review_data["doctor_id"]).first()
    doctor.average_rating = average_rating
    doctor.total_reviews = total_reviews

    db.commit()
    db.refresh(new_review)
    return {
        "review_id": new_review.review_id,
        "doctor_id": new_review.doctor_id,
        "patient_id": new_review.patient_id,
        "rating": new_review.rating,
        "review_text": new_review.review_text,
        "review_date": new_review.review_date,
    }
