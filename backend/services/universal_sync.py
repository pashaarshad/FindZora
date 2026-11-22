import os
import hashlib
from pathlib import Path
from datetime import datetime
from sqlalchemy.orm import Session
import cv2

from backend.config import BASE_DIR
from backend.database.models import Event, Photo, FaceRecord, ProcessingJob
from backend.face_engine.detector import get_face_detector
from backend.face_engine.recognizer import get_face_recognizer
from backend.vector_index.index_manager import vector_index_manager

SUPPORTED_EXTS = {".jpg", ".jpeg", ".png", ".webp"}

def calculate_sha256(file_path: Path) -> str:
    h = hashlib.sha256()
    with open(file_path, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()

def sync_universal_folder(db: Session):
    """
    Scans universal_folder/ and registers all event folders and photographs
    into SQLite database and vector search indices.
    """
    univ_dir = BASE_DIR / "universal_folder"
    if not univ_dir.exists():
        return

    detector = get_face_detector()
    recognizer = get_face_recognizer()

    for event_dir in univ_dir.iterdir():
        if not event_dir.is_dir() or event_dir.name.startswith("."):
            continue

        folder_name = event_dir.name
        # Human-readable event name
        event_name = folder_name.replace("_", " ").title()

        # Check or create Event in DB
        event = db.query(Event).filter(Event.name == event_name).first()
        if not event:
            event = Event(
                name=event_name,
                description=f"Auto-indexed event from Universal Folder: {folder_name}",
                organizer_name="Studio CLI Watcher",
                organizer_email="cli@findzora.local",
                retention_days=60,
                status="active"
            )
            db.add(event)
            db.commit()
            db.refresh(event)

        event_index = vector_index_manager.get_index(event.id)

        # Process each image in folder
        image_files = [f for f in event_dir.iterdir() if f.is_file() and f.suffix.lower() in SUPPORTED_EXTS]

        for img_path in image_files:
            file_hash = calculate_sha256(img_path)
            photo = db.query(Photo).filter(
                Photo.event_id == event.id,
                Photo.filename == img_path.name
            ).first()

            if photo and photo.status == "indexed":
                continue  # Already indexed

            img = cv2.imread(str(img_path))
            if img is None:
                continue

            h, w = img.shape[:2]
            if not photo:
                photo = Photo(
                    event_id=event.id,
                    filename=img_path.name,
                    file_path=str(img_path.resolve()),
                    file_hash=file_hash,
                    width=w,
                    height=h,
                    file_size=img_path.stat().st_size,
                    status="processing"
                )
                db.add(photo)
                db.commit()
                db.refresh(photo)

            # Detect faces
            faces = detector.detect_faces(img)
            valid_face_count = 0

            # Remove previous face records for idempotency
            db.query(FaceRecord).filter(FaceRecord.photo_id == photo.id).delete()

            for df in faces:
                if not df.is_usable:
                    continue

                emb = recognizer.generate_embedding(df.aligned_crop)

                face_rec = FaceRecord(
                    photo_id=photo.id,
                    event_id=event.id,
                    bbox_x=df.bbox[0],
                    bbox_y=df.bbox[1],
                    bbox_w=df.bbox[2],
                    bbox_h=df.bbox[3],
                    quality_score=df.quality_score,
                    blur_score=df.blur_score,
                    model_version="findzora_resnet18_v1"
                )
                db.add(face_rec)
                db.flush()

                event_index.add_face(
                    face_id=face_rec.id,
                    photo_id=photo.id,
                    embedding=emb
                )
                valid_face_count += 1

            photo.face_count = valid_face_count
            photo.status = "indexed"
            photo.file_path = str(img_path.resolve())
            db.commit()
            print(f"[UniversalSync] Indexed {photo.filename} in {event_name} ({valid_face_count} face(s)).")
