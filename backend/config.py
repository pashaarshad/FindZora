import os
from pathlib import Path

# Base Paths
BASE_DIR = Path(__file__).resolve().parent.parent
STORAGE_DIR = BASE_DIR / "storage"
PHOTOS_DIR = STORAGE_DIR / "photos"
TEMP_DIR = STORAGE_DIR / "temp"
DATABASE_DIR = BASE_DIR / "database"
DB_PATH = DATABASE_DIR / "findzora.db"
VECTOR_INDEX_DIR = DATABASE_DIR / "vector_indices"

# Ensure directories exist
PHOTOS_DIR.mkdir(parents=True, exist_ok=True)
TEMP_DIR.mkdir(parents=True, exist_ok=True)
DATABASE_DIR.mkdir(parents=True, exist_ok=True)
VECTOR_INDEX_DIR.mkdir(parents=True, exist_ok=True)

# Database Configuration
DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite:///{DB_PATH}")

# Face Recognition Settings
EMBEDDING_DIM = 512
SIMILARITY_THRESHOLD = float(os.getenv("SIMILARITY_THRESHOLD", "0.50"))
MIN_FACE_SIZE = int(os.getenv("MIN_FACE_SIZE", "40"))  # min face width/height in px
BLUR_THRESHOLD = float(os.getenv("BLUR_THRESHOLD", "35.0"))  # Laplacian variance threshold

# Security & Privacy Settings
EPHEMERAL_TEMP_CLEANUP = True
DEFAULT_RETENTION_DAYS = 30
ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}
MAX_FILE_SIZE_MB = 25
