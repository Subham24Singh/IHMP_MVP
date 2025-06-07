from sqlalchemy.orm import Session
from app.modules.ai_transcription.model import AITranscriptions
from app.modules.ai_transcription.schema import AITranscriptionsSchema
from typing import List

def create_ai_transcription_db(db: Session, transcription_data: AITranscriptionsSchema) -> AITranscriptions:
    new_transcription = AITranscriptions(**transcription_data.dict())
    db.add(new_transcription)
    db.commit()
    db.refresh(new_transcription)
    return new_transcription

def get_ai_transcriptions_by_user_id_db(db: Session, user_id: int) -> List[AITranscriptions]:
    return db.query(AITranscriptions).filter(AITranscriptions.user_id == user_id).all()

def get_ai_transcription_by_id_db(db: Session, transcription_id: int) -> AITranscriptions:
    return db.query(AITranscriptions).filter(AITranscriptions.id == transcription_id).first()

def update_ai_transcription_db(db: Session, transcription_id: int, transcription_data: AITranscriptionsSchema):
    transcription = db.query(AITranscriptions).filter(AITranscriptions.id == transcription_id).first()
    if not transcription:
        return None
    for field, value in transcription_data.dict(exclude_unset=True).items():
        setattr(transcription, field, value)
    db.commit()
    db.refresh(transcription)
    return transcription

def delete_ai_transcription_db(db: Session, transcription_id: int):
    transcription = db.query(AITranscriptions).filter(AITranscriptions.id == transcription_id).first()
    if not transcription:
        return False
    db.delete(transcription)
    db.commit()
    return True