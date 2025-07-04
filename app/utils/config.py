from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Access the env variable
DATABASE_URL = os.getenv("DATABASE_URL")
