from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.modules.doctor.models import Doctor
from app.modules.doctor.deps import get_current_doctor  # Dependency to get the authenticated doctor

router = APIRouter(prefix="/api/doctors", tags=["Doctors"])

# Get a particular doctor's profile
@router.get("/{doctor_id}")
def get_doctor_by_id(doctor_id: int, db: Session = Depends(get_db)):
    doctor = db.query(Doctor).filter(Doctor.id == doctor_id).first()
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    return {
        "id": doctor.id,
        "user_id": doctor.user_id,
        "full_name": doctor.full_name,
        "specialty": doctor.specialty,
        "bio": doctor.bio,
        "education": doctor.education,
        "experience": doctor.experience,
        "clinic_address": doctor.clinic_address,
        "photo_url": doctor.photo_url,
        "available_days": doctor.available_days,
        "time_slots": doctor.time_slots,
        "average_rating": getattr(doctor, 'average_rating', 0.0),
        "total_ratings": getattr(doctor, 'total_ratings', 0),
        "certifications": doctor.certifications,
        "languages_spoken": doctor.languages_spoken,
        "fees": doctor.fees,
        "insurance_accepted": doctor.insurance_accepted,
        "areas_of_expertise": doctor.areas_of_expertise
    }

# Get all doctors (public route)
@router.get("/", response_model=list[dict])
def get_all_doctors(db: Session = Depends(get_db)):
    doctors = db.query(Doctor).all()
    return [
        {
            "id": doctor.id,
            "user_id": doctor.user_id,
            "full_name": doctor.full_name,
            "specialty": doctor.specialty,
            "bio": doctor.bio,
            "education": doctor.education if doctor.education is not None else "",
            "experience": doctor.experience if doctor.experience is not None else "",
            "clinic_address": doctor.clinic_address,
            "photo_url": doctor.photo_url,
            "phone": getattr(doctor, 'phone', None),
            "email": getattr(doctor, 'email', None),
            "available_days": doctor.available_days,
            "time_slots": doctor.time_slots,
            "average_rating": getattr(doctor, 'average_rating', 0.0),
            "total_ratings": getattr(doctor, 'total_ratings', 0),
            "certifications": doctor.certifications if doctor.certifications is not None else "",
            "languages_spoken": doctor.languages_spoken,
            "fees": doctor.fees,
            "insurance_accepted": doctor.insurance_accepted,
            "areas_of_expertise": doctor.areas_of_expertise
        }
        for doctor in doctors
    ]

# Create a new doctor profile (secure route)
@router.post("/", response_model=dict)
def create_doctor_profile(doctor_data: dict, db: Session = Depends(get_db), current_doctor: Doctor = Depends(get_current_doctor)):
    # Check if the doctor already has a profile
    existing_profile = db.query(Doctor).filter(Doctor.id == current_doctor.id).first()
    if existing_profile:
        raise HTTPException(status_code=400, detail="Profile already exists for this doctor")

    # Prepare/convert fields as needed
    # Ensure languages_spoken is a list if provided as a string
    if 'languages_spoken' in doctor_data and isinstance(doctor_data['languages_spoken'], str):
        import json
        try:
            doctor_data['languages_spoken'] = json.loads(doctor_data['languages_spoken'])
        except Exception:
            doctor_data['languages_spoken'] = [doctor_data['languages_spoken']]
    # Ensure insurance_accepted is stored as integer (0/1)
    if 'insurance_accepted' in doctor_data:
        doctor_data['insurance_accepted'] = int(bool(doctor_data['insurance_accepted']))

    # Create a new profile with all fields
    new_doctor = Doctor(
        id=current_doctor.id,
        user_id=doctor_data.get('user_id'),
        full_name=doctor_data.get('full_name'),
        specialty=doctor_data.get('specialty'),
        bio=doctor_data.get('bio'),
        education=doctor_data.get('education'),
        experience=doctor_data.get('experience'),
        clinic_address=doctor_data.get('clinic_address'),
        photo_url=doctor_data.get('photo_url'),
        available_days=doctor_data.get('available_days'),
        time_slots=doctor_data.get('time_slots'),
        average_rating=doctor_data.get('average_rating', 0.0),
        total_ratings=doctor_data.get('total_ratings', 0),
        certifications=doctor_data.get('certifications'),
        languages_spoken=doctor_data.get('languages_spoken'),
        fees=doctor_data.get('fees'),
        insurance_accepted=doctor_data.get('insurance_accepted'),
        areas_of_expertise=doctor_data.get('areas_of_expertise')
    )
    db.add(new_doctor)
    db.commit()
    db.refresh(new_doctor)
    return {
        "id": new_doctor.id,
        "user_id": new_doctor.user_id,
        "full_name": new_doctor.full_name,
        "specialty": new_doctor.specialty,
        "bio": new_doctor.bio,
        "education": new_doctor.education if new_doctor.education is not None else "",
        "experience": new_doctor.experience if new_doctor.experience is not None else "",
        "clinic_address": new_doctor.clinic_address,
        "photo_url": new_doctor.photo_url,
        "phone": getattr(new_doctor, 'phone', None),
        "email": getattr(new_doctor, 'email', None),
        "available_days": new_doctor.available_days,
        "time_slots": new_doctor.time_slots,
        "average_rating": new_doctor.average_rating,
        "total_ratings": new_doctor.total_ratings,
        "certifications": new_doctor.certifications if new_doctor.certifications is not None else "",
        "languages_spoken": new_doctor.languages_spoken,
        "fees": new_doctor.fees,
        "insurance_accepted": new_doctor.insurance_accepted,
        "areas_of_expertise": new_doctor.areas_of_expertise
    }

# Update an existing doctor profile (secure route)
@router.put("/{doctor_id}", response_model=dict)
def update_doctor_profile(doctor_id: int, doctor_data: dict, db: Session = Depends(get_db), current_doctor: Doctor = Depends(get_current_doctor)):
    # Optionally: ensure only the owner/authorized user can update
    doctor = db.query(Doctor).filter(Doctor.id == doctor_id).first()
    if not doctor:
        raise HTTPException(status_code=404, detail="Profile not found")

    # Prepare/convert fields as needed
    if 'languages_spoken' in doctor_data and isinstance(doctor_data['languages_spoken'], str):
        import json
        try:
            doctor_data['languages_spoken'] = json.loads(doctor_data['languages_spoken'])
        except Exception:
            doctor_data['languages_spoken'] = [doctor_data['languages_spoken']]
    if 'insurance_accepted' in doctor_data:
        doctor_data['insurance_accepted'] = int(bool(doctor_data['insurance_accepted']))

    # Update the profile
    for key, value in doctor_data.items():
        setattr(doctor, key, value)

    db.commit()
    db.refresh(doctor)
    return {
        "id": doctor.id,
        "user_id": doctor.user_id,
        "full_name": doctor.full_name,
        "specialty": doctor.specialty,
        "bio": doctor.bio,
        "education": doctor.education,
        "experience": doctor.experience,
        "clinic_address": doctor.clinic_address,
        "photo_url": doctor.photo_url,
        "available_days": doctor.available_days,
        "time_slots": doctor.time_slots,
        "average_rating": getattr(doctor, 'average_rating', 0.0),
        "total_ratings": getattr(doctor, 'total_ratings', 0),
        "certifications": doctor.certifications,
        "languages_spoken": doctor.languages_spoken,
        "fees": doctor.fees,
        "insurance_accepted": doctor.insurance_accepted,
        "areas_of_expertise": doctor.areas_of_expertise
    }
      