from sqlalchemy import JSON, Column, DateTime, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database.database import Base
from datetime import datetime

class AITranscriptions(Base):
     __tablename__ = "ai_transcriptions"
     
     id = Column(Integer, primary_key=True, index=True, autoincrement=True)
     user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False)
     transcription_data = Column(JSON, nullable=False)  # JSONB for AI-generated transcriptions
     created_at = Column(DateTime, default=datetime.utcnow, nullable=False)