import os
import uuid
import hashlib
import cv2
import numpy as np
from pathlib import Path
from sqlalchemy.orm import Session
from fastapi import HTTPException
from backend.config import TEMP_DIR, SIMILARITY_THRESHOLD
from backend.database.models import Event, Photo, ConsentLog, WrongMatchReport
from backend.face_engine.detector import get_face_detector
from backend.face_engine.recognizer import get_face_recognizer
from backend.vector_index.index_manager import vector_index_manager

class SearchService:
    @staticmethod
    def record_consent(
        db: Session,
        event_id: str,
        attendee_name: str = "Anonymous Attendee",
        client_ip: str = "127.0.0.1"
    ) -> ConsentLog:
        """Records attendee informed consent as required by biometric regulations."""
        ip_hash = hashlib.sha256(client_ip.encode()).hexdigest()
        consent = ConsentLog(
            event_id=event_id,
            attendee_name=attendee_name,
            consent_version="FindZora_Consent_v2.0",
            ip_hash=ip_hash
        )
        db.add(consent)
        db.commit()
        db.refresh(consent)
        return consent

    @staticmethod
    def search_by_selfie(
        db: Session,
        event_id: str,
        selfie_bytes: bytes,
        threshold: float = SIMILARITY_THRESHOLD,
        top_k: int = 50
    ) -> dict:
        """
        Executes privacy-preserving selfie search:
        1. Decode query image
        2. Detect query face & verify single clear face
        3. Generate 512-D embedding
        4. Query isolated event vector index
        5. Purge temporary image data immediately
        6. Return ranked candidate photos
        """
        event = db.query(Event).filter(Event.id == event_id, Event.status == "active").first()
        if not event:
            raise HTTPException(status_code=404, detail="Event not found or inactive.")

        # Decode selfie image
        nparr = np.frombuffer(selfie_bytes, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        if img is None:
            raise HTTPException(status_code=400, detail="Invalid image file or camera capture corrupted.")

        detector = get_face_detector()
        faces = detector.detect_faces(img)

        if len(faces) == 0:
            raise HTTPException(
                status_code=422,
                detail="No face detected in your capture. Please position your face clearly in good lighting and try again."
            )

        # Select the most prominent face if multiple found
        usable_faces = [f for f in faces if f.is_usable]
        if not usable_faces:
            first_fail = faces[0].filter_reason
            raise HTTPException(
                status_code=422,
                detail=f"Selfie quality check failed: {first_fail}. Please retake with a clear, well-lit frontal view."
            )

        # Pick best face by quality
        best_face = max(usable_faces, key=lambda f: f.quality_score)

        # Generate 512-D query embedding
        recognizer = get_face_recognizer()
        query_embedding = recognizer.generate_embedding(best_face.aligned_crop)

        # Query isolated event index
        event_index = vector_index_manager.get_index(event_id)
        candidates = event_index.search(query_embedding, top_k=top_k, threshold=threshold)

        # Populate photo details for matches
        results = []
        for c in candidates:
            photo = db.query(Photo).filter(Photo.id == c.photo_id).first()
            if photo:
                results.append({
                    "photo_id": photo.id,
                    "filename": photo.filename,
                    "similarity": round(c.similarity, 4),
                    "confidence_percentage": round(c.similarity * 100, 1),
                    "image_url": f"/api/photos/{photo.id}/stream",
                    "width": photo.width,
                    "height": photo.height,
                    "created_at": photo.created_at.isoformat()
                })

        return {
            "event_id": event_id,
            "event_name": event.name,
            "threshold_applied": threshold,
            "total_matches": len(results),
            "candidates": results,
            "biometric_notice": "Your query selfie was processed in memory and has been permanently deleted as per FindZora privacy policy."
        }

    @staticmethod
    def search_universal_by_selfie(
        db: Session,
        selfie_bytes: bytes,
        threshold: float = SIMILARITY_THRESHOLD,
        top_k_per_event: int = 50
    ) -> dict:
        """
        Universal Multi-Event Discovery:
        Searches across all active events with a single selfie capture.
        Groups candidate photos by event for convenient single-click event downloads.
        """
        # Decode selfie image
        nparr = np.frombuffer(selfie_bytes, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        if img is None:
            raise HTTPException(status_code=400, detail="Invalid selfie image data.")

        detector = get_face_detector()
        faces = detector.detect_faces(img)

        if len(faces) == 0:
            raise HTTPException(status_code=422, detail="No face detected in selfie.")

        usable_faces = [f for f in faces if f.is_usable]
        if not usable_faces:
            raise HTTPException(status_code=422, detail="Selfie does not meet quality requirements.")

        best_face = max(usable_faces, key=lambda f: f.quality_score)
        recognizer = get_face_recognizer()
        query_embedding = recognizer.generate_embedding(best_face.aligned_crop)

        # Iterate through all active events
        active_events = db.query(Event).filter(Event.status == "active").all()
        grouped_results = []
        total_photos = 0

        for ev in active_events:
            ev_index = vector_index_manager.get_index(ev.id)
            candidates = ev_index.search(query_embedding, top_k=top_k_per_event, threshold=threshold)
            if candidates:
                event_photos = []
                for c in candidates:
                    photo = db.query(Photo).filter(Photo.id == c.photo_id).first()
                    if photo:
                        event_photos.append({
                            "photo_id": photo.id,
                            "filename": photo.filename,
                            "similarity": round(c.similarity, 4),
                            "confidence_percentage": round(c.similarity * 100, 1),
                            "image_url": f"/api/photos/{photo.id}/stream",
                            "width": photo.width,
                            "height": photo.height,
                            "created_at": photo.created_at.isoformat()
                        })
                if event_photos:
                    total_photos += len(event_photos)
                    grouped_results.append({
                        "event_id": ev.id,
                        "event_name": ev.name,
                        "description": ev.description,
                        "organizer_name": ev.organizer_name,
                        "created_at": ev.created_at.isoformat(),
                        "total_matches": len(event_photos),
                        "photos": event_photos
                    })

        return {
            "total_events_matched": len(grouped_results),
            "total_photos_matched": total_photos,
            "threshold_applied": threshold,
            "grouped_events": grouped_results,
            "biometric_notice": "Query selfie processed ephemerally and deleted as per FindZora privacy policy."
        }

    @staticmethod
    def submit_wrong_match_report(
        db: Session,
        event_id: str,
        photo_id: str,
        attendee_notes: str
    ) -> WrongMatchReport:
        report = WrongMatchReport(
            event_id=event_id,
            photo_id=photo_id,
            attendee_notes=attendee_notes.strip()
        )
        db.add(report)
        db.commit()
        db.refresh(report)
        return report
