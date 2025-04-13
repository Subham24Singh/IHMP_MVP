import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

class Settings:
    DATABASE_URL = os.getenv("DATABASE_URL")

# Instantiate the settings
settings = Settings()
