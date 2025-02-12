import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
UPLOAD_FOLDER = "uploads"
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

# Supported image extensions
ALLOWED_EXTENSIONS = {
    "text": [".txt", ".md"],
    "image": [".png", ".jpg", ".jpeg"],
    "audio": [".mp3", ".wav"],
}
