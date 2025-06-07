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

patient_ai_transcription_router = APIRouter(
    prefix="/transcriptions",
    tags=["Patient AI Transcriptions"],
    dependencies=[Depends(require_role(["Patient"]))]
)

@patient_ai_transcription_router.post("/", response_model=AITranscriptionsSchema, status_code=status.HTTP_201_CREATED)
async def patient_create_ai_transcription(
    transcription: AITranscriptionsSchema,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Only allow if user_id matches current user
    if transcription.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Cannot create for another user.")
    return create_ai_transcription_db(db, transcription)

@patient_ai_transcription_router.get("/", response_model=List[AITranscriptionsSchema])
async def patient_get_own_transcriptions(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_ai_transcriptions_by_user_id_db(db, current_user.id) or []

@patient_ai_transcription_router.get("/{transcription_id}", response_model=AITranscriptionsSchema)
async def patient_get_own_transcription_by_id(
    transcription_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    transcription = get_ai_transcription_by_id_db(db, transcription_id)
    if not transcription or transcription.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Transcription not found.")
    return transcription