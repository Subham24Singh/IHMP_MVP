from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.modules.ai_transcription.schema import AITranscriptionsSchema
from app.database.database import get_db
from app.modules.user.deps import get_current_user
from app.modules.user.model import User
from app.rbac import require_role
from app.modules.ai_transcription.routes import (
    create_ai_transcription_db,
    get_ai_transcriptions_by_user_id_db,
    get_ai_transcription_by_id_db,
)
from app.modules.doctor.utils import has_appointment_with_patient

doctor_ai_transcription_router = APIRouter(
    prefix="/transcriptions",
    tags=["Doctor AI Transcriptions"],
    dependencies=[Depends(require_role(["Doctor"]))]
)

@doctor_ai_transcription_router.post("/patient/{patient_id}", response_model=AITranscriptionsSchema, status_code=status.HTTP_201_CREATED)
async def doctor_create_patient_transcription(
    patient_id: int,
    transcription: AITranscriptionsSchema,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Only allow if doctor has appointment with this patient
    if not has_appointment_with_patient(db, doctor_id=current_user.id, patient_id=patient_id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No appointment with this patient.")
    if transcription.user_id != patient_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="user_id mismatch.")
    return create_ai_transcription_db(db, transcription)

@doctor_ai_transcription_router.get("/patient/{patient_id}", response_model=List[AITranscriptionsSchema])
async def doctor_get_patient_transcriptions(
    patient_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not has_appointment_with_patient(db, doctor_id=current_user.id, patient_id=patient_id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No appointment with this patient.")
    return get_ai_transcriptions_by_user_id_db(db, patient_id) or []

@doctor_ai_transcription_router.get("/{transcription_id}", response_model=AITranscriptionsSchema)
async def doctor_get_transcription_by_id(
    transcription_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    transcription = get_ai_transcription_by_id_db(db, transcription_id)
    if not transcription or not has_appointment_with_patient(db, doctor_id=current_user.id, patient_id=transcription.user_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Transcription not found or not authorized.")
    return transcription