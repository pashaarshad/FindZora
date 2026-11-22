from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.database.connection import get_db
from backend.database.models import ProcessingJob, WrongMatchReport, Event, Photo, FaceRecord
from backend.workers.image_processor import process_photo_job

router = APIRouter(prefix="/api/admin", tags=["Admin & Developer Dashboard"])

@router.get("/jobs")
def list_processing_jobs(db: Session = Depends(get_db)):
    jobs = db.query(ProcessingJob).order_by(ProcessingJob.created_at.desc()).limit(100).all()
    return [
        {
            "id": j.id,
            "photo_id": j.photo_id,
            "event_id": j.event_id,
            "status": j.status,
            "attempts": j.attempts,
            "error_message": j.error_message,
            "created_at": j.created_at.isoformat(),
            "updated_at": j.updated_at.isoformat()
        }
        for j in jobs
    ]

@router.post("/jobs/{job_id}/retry")
def retry_job(job_id: str, db: Session = Depends(get_db)):
    job = db.query(ProcessingJob).filter(ProcessingJob.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    process_photo_job(job_id, db)
    db.refresh(job)
    return {"message": "Job retry triggered", "job_id": job.id, "status": job.status}

@router.get("/reports")
def list_reports(db: Session = Depends(get_db)):
    reports = db.query(WrongMatchReport).order_by(WrongMatchReport.created_at.desc()).all()
    return [
        {
            "id": r.id,
            "event_id": r.event_id,
            "photo_id": r.photo_id,
            "attendee_notes": r.attendee_notes,
            "status": r.status,
            "created_at": r.created_at.isoformat()
        }
        for r in reports
    ]

@router.post("/reports/{report_id}/resolve")
def resolve_report(report_id: str, status: str = "confirmed_incorrect", db: Session = Depends(get_db)):
    report = db.query(WrongMatchReport).filter(WrongMatchReport.id == report_id).first()
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    report.status = status
    db.commit()
    return {"message": "Report status updated", "status": report.status}

@router.get("/stats")
def get_system_stats(db: Session = Depends(get_db)):
    total_events = db.query(Event).filter(Event.status == "active").count()
    total_photos = db.query(Photo).count()
    total_indexed_faces = db.query(FaceRecord).count()
    failed_jobs = db.query(ProcessingJob).filter(ProcessingJob.status == "failed").count()
    pending_reports = db.query(WrongMatchReport).filter(WrongMatchReport.status == "pending_review").count()

    return {
        "active_events": total_events,
        "total_photos": total_photos,
        "indexed_faces": total_indexed_faces,
        "failed_jobs": failed_jobs,
        "pending_wrong_match_reports": pending_reports
    }

@router.get("/watch-folder")
def get_watch_folder_info():
    """Returns the Universal Folder status, detected event folders, and cluster indexes."""
    import json
    from pathlib import Path
    from backend.config import BASE_DIR

    univ_path = BASE_DIR / "universal_folder"
    events_found = []

    if univ_path.exists():
        for item in univ_path.iterdir():
            if item.is_dir() and not item.name.startswith("."):
                index_file = item / "face_clusters.json"
                clusters_count = 0
                photos_count = len([f for f in item.iterdir() if f.suffix.lower() in {".jpg", ".jpeg", ".png"}])
                sample_clusters = {}

                if index_file.exists():
                    try:
                        with open(index_file, "r", encoding="utf-8") as f:
                            cdata = json.load(f)
                            clusters_count = len(cdata.get("person_clusters", {}))
                            sample_clusters = cdata.get("person_clusters", {})
                    except Exception:
                        pass

                events_found.append({
                    "folder_name": item.name,
                    "photos_count": photos_count,
                    "clusters_count": clusters_count,
                    "has_index": index_file.exists(),
                    "sample_clusters": sample_clusters
                })

    return {
        "watch_dir": str(univ_path),
        "status": "watching",
        "events_count": len(events_found),
        "events": events_found
    }
