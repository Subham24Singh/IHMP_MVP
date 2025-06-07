from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.modules.doctor.deps import get_current_doctor  # Role check for doctors
from app.modules.allergytracking.models import AllergyTracking  # AllergyTracking model
from app.modules.allergytracking.schema import AllergyTrackingCreate  # Schema for input
from app.modules.user.model import User  # User model
from app.rbac import require_role

router = APIRouter(dependencies=[Depends(require_role(["Doctor"]))])

# Get allergy details for a specific patient
@router.get("/{patient_id}", response_model=List[AllergyTrackingCreate])
def get_allergies(
    patient_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_doctor)  # Ensure the user is a doctor
):
    # Ensure the doctor is authorized to view this patient's allergies
    patient_allergies = db.query(AllergyTracking).filter(AllergyTracking.user_id == patient_id).all()
    
    if not patient_allergies:
        raise HTTPException(status_code=404, detail="Allergy data not found for this patient")
    
    return patient_allergies

# Add or update allergy information for a patient
@router.post("/", status_code=201)
def add_allergy(
    allergy_data: AllergyTrackingCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_doctor)  # Ensure the user is a doctor
):
    # Check if the allergy already exists for the patient
    existing_allergy = db.query(AllergyTracking).filter(
        AllergyTracking.user_id == allergy_data.user_id,
        AllergyTracking.allergy_name == allergy_data.allergy_name
    ).first()
    
    if existing_allergy:
        # Update the existing allergy record
        existing_allergy.reaction = allergy_data.reaction
        db.commit()
        db.refresh(existing_allergy)
        return {"message": "Allergy updated successfully", "allergy": existing_allergy}
    
    # If not exists, create a new allergy record
    new_allergy = AllergyTracking(
        user_id=allergy_data.user_id,
        allergy_name=allergy_data.allergy_name,
        reaction=allergy_data.reaction
    )
    db.add(new_allergy)
    db.commit()
    db.refresh(new_allergy)
    
    return {
        "message": "Allergy added successfully",
        "allergy": {
            "allergy_id": new_allergy.allergy_id,
            "user_id": new_allergy.user_id,
            "allergy_name": new_allergy.allergy_name,
            "reaction": new_allergy.reaction
        }
    }
