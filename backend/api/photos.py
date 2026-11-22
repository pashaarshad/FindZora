from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from pathlib import Path
from backend.database.connection import get_db
from backend.database.models import Photo
from backend.services.photo_service import PhotoService

router = APIRouter(tags=["Photos"])

@router.post("/api/events/{event_id}/photos/batch")
async def upload_batch_photos(
    event_id: str,
    files: list[UploadFile] = File(...),
    db: Session = Depends(get_db)
):
    results = []
    duplicates = 0
    errors = []

    for file in files:
        try:
            photo, is_duplicate = await PhotoService.save_uploaded_photo(db, event_id, file)
            if is_duplicate:
                duplicates += 1
                results.append({"filename": file.filename, "status": "duplicate_skipped", "photo_id": photo.id})
            else:
                results.append({"filename": file.filename, "status": "uploaded_and_queued", "photo_id": photo.id})
        except Exception as e:
            errors.append({"filename": file.filename, "error": str(e)})

    return {
        "event_id": event_id,
        "total_files": len(files),
        "successful": len(results) - duplicates,
        "duplicates_skipped": duplicates,
        "errors": errors,
        "details": results
    }

@router.get("/api/events/{event_id}/photos")
def list_event_photos(event_id: str, db: Session = Depends(get_db)):
    photos = db.query(Photo).filter(Photo.event_id == event_id).order_by(Photo.created_at.desc()).all()
    return [
        {
            "id": p.id,
            "filename": p.filename,
            "status": p.status,
            "face_count": p.face_count,
            "width": p.width,
            "height": p.height,
            "file_size": p.file_size,
            "created_at": p.created_at.isoformat(),
            "stream_url": f"/api/photos/{p.id}/stream"
        }
        for p in photos
    ]

@router.get("/api/photos/{photo_id}/stream")
def stream_photo(photo_id: str, db: Session = Depends(get_db)):
    """Streams the private image file securely."""
    photo = db.query(Photo).filter(Photo.id == photo_id).first()
    if not photo or not Path(photo.file_path).exists():
        raise HTTPException(status_code=404, detail="Photo not found")
    suffix = Path(photo.file_path).suffix.lower()
    media_type = "image/png" if suffix == ".png" else "image/jpeg"
    return FileResponse(photo.file_path, media_type=media_type)

@router.get("/api/photos/{photo_id}/faces")
def get_detected_faces(photo_id: str, db: Session = Depends(get_db)):
    """Developer/Admin inspector endpoint returning face bounding boxes and quality metrics."""
    faces = PhotoService.get_photo_faces(db, photo_id)
    return {"photo_id": photo_id, "faces": faces}
