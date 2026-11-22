import cv2
import traceback
from datetime import datetime
from sqlalchemy.orm import Session
from backend.database.models import Photo, FaceRecord, ProcessingJob
from backend.face_engine.detector import get_face_detector
from backend.face_engine.recognizer import get_face_recognizer
from backend.vector_index.index_manager import vector_index_manager

def process_photo_job(job_id: str, db: Session):
    """
    Executes the ingestion pipeline on a single photo job:
    1. Read photo from private storage
    2. Detect all faces & filter by quality gate
    3. Generate 512-D embeddings for usable faces
    4. Save FaceRecords in SQLite
    5. Add embeddings to isolated event vector index
    6. Update Photo status to indexed and Job to completed
    """
    job = db.query(ProcessingJob).filter(ProcessingJob.id == job_id).first()
    if not job:
        return

    job.status = "processing"
    job.attempts += 1
    job.updated_at = datetime.utcnow()
    db.commit()

    photo = db.query(Photo).filter(Photo.id == job.photo_id).first()
    if not photo:
        job.status = "failed"
        job.error_message = "Photo record not found"
        db.commit()
        return

    try:
        # Load image
        img = cv2.imread(photo.file_path)
        if img is None:
            raise ValueError(f"Unable to decode image from private storage: {photo.file_path}")

        h, w = img.shape[:2]
        photo.width = w
        photo.height = h

        # Detect multiple faces
        detector = get_face_detector()
        detected_faces = detector.detect_faces(img)

        recognizer = get_face_recognizer()
        event_index = vector_index_manager.get_index(photo.event_id)

        valid_face_count = 0

        # Purge any existing face records for this photo before re-processing (idempotency)
        db.query(FaceRecord).filter(FaceRecord.photo_id == photo.id).delete()

        for df in detected_faces:
            if not df.is_usable:
                continue

            # Generate 512-D embedding
            emb = recognizer.generate_embedding(df.aligned_crop)

            # Create FaceRecord in DB
            face_rec = FaceRecord(
                photo_id=photo.id,
                event_id=photo.event_id,
                bbox_x=df.bbox[0],
                bbox_y=df.bbox[1],
                bbox_w=df.bbox[2],
                bbox_h=df.bbox[3],
                quality_score=df.quality_score,
                blur_score=df.blur_score,
                model_version="findzora_arcface_v1"
            )
            db.add(face_rec)
            db.flush()  # Populates face_rec.id

            # Add to event vector index
            event_index.add_face(
                face_id=face_rec.id,
                photo_id=photo.id,
                embedding=emb
            )

            valid_face_count += 1

        photo.face_count = valid_face_count
        photo.status = "indexed"
        job.status = "completed"
        job.error_message = None
        job.updated_at = datetime.utcnow()
        db.commit()

    except Exception as e:
        db.rollback()
        job = db.query(ProcessingJob).filter(ProcessingJob.id == job_id).first()
        if job:
            job.status = "failed"
            job.error_message = f"{str(e)}\n{traceback.format_exc()}"
            job.updated_at = datetime.utcnow()
        if photo:
            photo = db.query(Photo).filter(Photo.id == job.photo_id).first()
            if photo:
                photo.status = "failed"
        db.commit()
