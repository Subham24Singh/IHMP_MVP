import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

class Settings:
    DATABASE_URL = "postgresql://postgres:Pi%40122912@localhost:5432/ihmp_db"
    TIMEZONE: str = os.getenv("TIMEZONE", "Asia/Kolkata") 

# Instantiate the settings
settings = Settings()
