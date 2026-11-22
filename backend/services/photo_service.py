import hashlib
import uuid
from pathlib import Path
from sqlalchemy.orm import Session
from fastapi import UploadFile, HTTPException
from backend.config import PHOTOS_DIR, ALLOWED_EXTENSIONS, MAX_FILE_SIZE_MB
from backend.database.models import Photo, ProcessingJob, FaceRecord
from backend.workers.image_processor import process_photo_job

class PhotoService:
    @staticmethod
    def calculate_file_hash(content: bytes) -> str:
        return hashlib.sha256(content).hexdigest()

    @staticmethod
    async def save_uploaded_photo(
        db: Session,
        event_id: str,
        upload_file: UploadFile
    ) -> tuple[Photo, bool]:
        """
        Saves photo securely in private storage and initiates processing.
        Detects duplicates via SHA-256 hash.
        Returns: (Photo, is_duplicate: bool)
        """
        # Validate extension
        suffix = Path(upload_file.filename).suffix.lower()
        if suffix not in ALLOWED_EXTENSIONS:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported file format '{suffix}'. Allowed: {', '.join(ALLOWED_EXTENSIONS)}"
            )

        content = await upload_file.read()
        file_size = len(content)

        if file_size > MAX_FILE_SIZE_MB * 1024 * 1024:
            raise HTTPException(
                status_code=400,
                detail=f"File exceeds maximum allowed size of {MAX_FILE_SIZE_MB}MB."
            )

        file_hash = PhotoService.calculate_file_hash(content)

        # Check for duplicate upload within the event
        existing_photo = db.query(Photo).filter(
            Photo.event_id == event_id,
            Photo.file_hash == file_hash
        ).first()

        if existing_photo:
            return existing_photo, True

        # Generate unique photo ID and storage path
        photo_id = str(uuid.uuid4())
        safe_filename = f"{photo_id}{suffix}"
        target_path = PHOTOS_DIR / safe_filename

        with open(target_path, "wb") as f:
            f.write(content)

        photo = Photo(
            id=photo_id,
            event_id=event_id,
            filename=upload_file.filename,
            file_path=str(target_path),
            file_hash=file_hash,
            file_size=file_size,
            status="uploaded"
        )
        db.add(photo)
        db.flush()

        # Create processing job
        job = ProcessingJob(
            photo_id=photo.id,
            event_id=event_id,
            status="queued"
        )
        db.add(job)
        db.commit()
        db.refresh(photo)

        # Execute processing worker
        process_photo_job(job.id, db)

        return photo, False

    @staticmethod
    def get_photo_faces(db: Session, photo_id: str) -> list[dict]:
        """Returns detected face bounding boxes and quality metrics for developer/admin view."""
        faces = db.query(FaceRecord).filter(FaceRecord.photo_id == photo_id).all()
        return [
            {
                "id": f.id,
                "bbox": [f.bbox_x, f.bbox_y, f.bbox_w, f.bbox_h],
                "quality_score": f.quality_score,
                "blur_score": f.blur_score,
                "model_version": f.model_version
            }
            for f in faces
        ]
