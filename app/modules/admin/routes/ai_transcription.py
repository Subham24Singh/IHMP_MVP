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
    delete_ai_transcription_db,
    update_ai_transcription_db
)

admin_ai_transcription_router = APIRouter(
    prefix="/transcriptions",
    tags=["Admin AI Transcriptions"],
    dependencies=[Depends(require_role(["Admin"]))]
)

@admin_ai_transcription_router.post("/", response_model=AITranscriptionsSchema, status_code=status.HTTP_201_CREATED)
async def admin_create_ai_transcription(
    transcription: AITranscriptionsSchema,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return create_ai_transcription_db(db, transcription)

@admin_ai_transcription_router.get("/user/{user_id}", response_model=List[AITranscriptionsSchema])
async def admin_get_ai_transcriptions_by_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_ai_transcriptions_by_user_id_db(db, user_id) or []

@admin_ai_transcription_router.get("/{transcription_id}", response_model=AITranscriptionsSchema)
async def admin_get_ai_transcription_by_id(
    transcription_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    transcription = get_ai_transcription_by_id_db(db, transcription_id)
    if not transcription:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Transcription not found.")
    return transcription

@admin_ai_transcription_router.delete("/{transcription_id}", status_code=status.HTTP_204_NO_CONTENT)
async def admin_delete_ai_transcription(
    transcription_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    success = delete_ai_transcription_db(db, transcription_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Transcription not found.")
    return

@admin_ai_transcription_router.put("/{transcription_id}", response_model=AITranscriptionsSchema)
async def admin_update_ai_transcription(
    transcription_id: int,
    transcription: AITranscriptionsSchema,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    updated = update_ai_transcription_db(db, transcription_id, transcription)
    if not updated:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Transcription not found.")
    return updated