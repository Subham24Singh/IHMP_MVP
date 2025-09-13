from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import date, time
from app.database.database import get_db
from app.modules.doctor.models import AvailabilitySlot, SlotStatus, Doctor
from app.modules.doctor.deps import get_current_doctor

router = APIRouter(prefix="/api/doctors", tags=["Availability"])

# POST /doctors/{doctor_id}/availability
@router.post("/{doctor_id}/availability", response_model=dict)
def add_availability_slot(
    doctor_id: int,
    slot_data: dict,
    db: Session = Depends(get_db),
    current_doctor: Doctor = Depends(get_current_doctor),
):
    # Fetch the doctor profile associated with the authenticated user
    doctor_profile = db.query(Doctor).filter(Doctor.id == current_doctor.id).first()
    if not doctor_profile:
        raise HTTPException(status_code=404, detail="Doctor profile not found")

    if doctor_id != doctor_profile.id:
        raise HTTPException(status_code=403, detail="Not authorized to manage this doctor's availability")

    new_slot = AvailabilitySlot(
        doctor_id=doctor_id,
        slot_date=slot_data["slot_date"],
        start_time=slot_data["start_time"],
        end_time=slot_data["end_time"],
        status=SlotStatus.AVAILABLE,
    )
    db.add(new_slot)
    db.commit()
    db.refresh(new_slot)
    return {
        "slot_id": new_slot.slot_id,
        "slot_date": new_slot.slot_date,
        "start_time": new_slot.start_time,
        "end_time": new_slot.end_time,
        "status": new_slot.status.value,
    }

# GET /doctors/{doctor_id}/availability
@router.get("/{doctor_id}/availability", response_model=list[dict])
def get_availability_slots(
    doctor_id: int,
    db: Session = Depends(get_db),
):
    slots = db.query(AvailabilitySlot).filter(AvailabilitySlot.doctor_id == doctor_id).all()
    return [
        {
            "slot_id": slot.slot_id,
            "slot_date": slot.slot_date,
            "start_time": slot.start_time,
            "end_time": slot.end_time,
            "status": slot.status.value,
        }
        for slot in slots
    ]

# PUT /doctors/{doctor_id}/availability/{slot_id}
@router.put("/{doctor_id}/availability/{slot_id}", response_model=dict)
def update_availability_slot(
    doctor_id: int,
    slot_id: int,
    slot_data: dict,
    db: Session = Depends(get_db),
    current_doctor: Doctor = Depends(get_current_doctor),
):
    # Fetch the doctor profile associated with the authenticated user
    doctor_profile = db.query(Doctor).filter(Doctor.id == current_doctor.id).first()
    if not doctor_profile:
        raise HTTPException(status_code=404, detail="Doctor profile not found")

    if doctor_id != doctor_profile.id:
        raise HTTPException(status_code=403, detail="Not authorized to manage this doctor's availability")

    # Ensure the slot_id is correctly mapped and validated
    slot = db.query(AvailabilitySlot).filter(
        AvailabilitySlot.slot_id == slot_id,
        AvailabilitySlot.doctor_id == doctor_id
    ).first()

    if not slot:
        raise HTTPException(status_code=404, detail="Availability slot not found")

    # Update the slot details
    for key, value in slot_data.items():
        if hasattr(slot, key):
            setattr(slot, key, value)
        else:
            raise HTTPException(status_code=400, detail=f"Invalid field: {key}")

    # Normalize the status value to uppercase to handle case-insensitive input
    if "status" in slot_data:
        slot_data["status"] = slot_data["status"].strip().upper()
        if slot_data["status"] not in [e.name for e in SlotStatus]:
            raise HTTPException(status_code=400, detail=f"Invalid status value: {slot_data['status']}")

    db.commit()
    db.refresh(slot)
    return {
        "slot_id": slot.slot_id,
        "slot_date": slot.slot_date,
        "start_time": slot.start_time,
        "end_time": slot.end_time,
        "status": slot.status.value,
    }
