from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.config import settings  # Ensure correct import

# Define the Base class
Base = declarative_base()

# Database URL from settings
DATABASE_URL = settings.DATABASE_URL

# Create Engine
engine = create_engine(DATABASE_URL)

# Create Session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()