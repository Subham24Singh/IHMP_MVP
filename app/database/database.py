from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.config import settings
import sys

# Define the Base class
Base = declarative_base()

# Database URL from settings
DATABASE_URL = settings.DATABASE_URL

if not DATABASE_URL or "postgresql://" not in DATABASE_URL:
    print("ERROR: DATABASE_URL is not set or is invalid. Please check your .env file.", file=sys.stderr)
    sys.exit(1)

# Ensure the correct driver is used for Postgres
if DATABASE_URL.startswith("postgresql://") and "+psycopg2" not in DATABASE_URL:
    DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+psycopg2://", 1)

try:
    engine = create_engine(DATABASE_URL)
except Exception as e:
    print(f"ERROR: Could not create engine with DATABASE_URL '{DATABASE_URL}': {e}", file=sys.stderr)
    sys.exit(1)

# Create Session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()