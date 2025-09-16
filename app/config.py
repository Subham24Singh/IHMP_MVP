import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

class Settings:
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://postgres:Manu2413@localhost:5432/ihmp_db")
    SECRET_KEY: str = os.getenv("SECRET_KEY", "testsecret")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
    TIMEZONE: str = os.getenv("TIMEZONE", "Asia/Kolkata")

# Instantiate the settings
settings = Settings()
