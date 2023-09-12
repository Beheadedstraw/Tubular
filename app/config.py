import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Define environment variables
HOST = os.environ.get("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", 8000))
CONFIG_DIR = os.getenv("CONFIG_DIR", "/data")
DOWNLOAD_DIR = os.getenv("DOWNLOAD_DIR", "/videos")