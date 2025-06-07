# app/modules/appointment/schema.py
from pydantic import BaseModel, Field
from datetime import datetime
from app.modules.enum.models import StatusEnum # Assuming StatusEnum is correctly defined here

# --- REVISED AppointmentCreate ---
# patient_id is REMOVED from this schema. It will be derived from the authenticated user.
class AppointmentCreate(BaseModel):
    doctor_id: int = Field(..., description="ID of the doctor for the appointment")
    appointment_date: datetime = Field(..., description="Date and time of the appointment")
    # If you want to add a 'reason' field, add it here:
    # reason: str = Field(None, description="Reason for the appointment")

# --- AppointmentResponse (Keep as is, but ensure 'status' is correct) ---
class AppointmentResponse(BaseModel):
    appointment_id: int
    patient_id: int
    doctor_id: int
    appointment_date: datetime
    # Ensure this matches your model, which uses String(50) now.
    # If StatusEnum is just for Pydantic validation, it's fine.
    # If your DB column is literally an Enum type, keep Enum.
    # If it's a String, then make this 'str'
    status: str # Changed to str to match your model.py's Column(String(50))
    # If you add 'reason' to AppointmentCreate, add it here too:
    # reason: str = None

    class Config:
        from_attributes = True # Modern Pydantic (v2+)
        # orm_mode = True # For older Pydantic (v1.x)