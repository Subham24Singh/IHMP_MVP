from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.models.ai_transcriptions import AITranscriptions
from app.schemas.ai_transcriptions import AITranscriptionsSchema
from app.database.database import SessionLocal

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/")
def create_ai_transcription(transcription: AITranscriptionsSchema, db: Session = Depends(get_db)):
    new_transcription = AITranscriptions(**transcription.dict())
    db.add(new_transcription)
    db.commit()
    db.refresh(new_transcription)
    return {"message": "AI Transcription created", "transcription_id": new_transcription.id}

@router.get("/{patient_id}")
def get_ai_transcriptions(patient_id: int, db: Session = Depends(get_db)):
    transcriptions = db.query(AITranscriptions).filter(AITranscriptions.user_id == patient_id).all()
    if not transcriptions:
        raise HTTPException(status_code=404, detail="No AI transcriptions found")
    return {"ai_transcriptions": transcriptions}
