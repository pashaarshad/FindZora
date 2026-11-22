from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from backend.database.models import Event, Photo
from backend.vector_index.index_manager import vector_index_manager
from pathlib import Path

class EventService:
    @staticmethod
    def create_event(
        db: Session,
        name: str,
        organizer_name: str,
        organizer_email: str,
        description: str = "",
        passcode: str = None,
        retention_days: int = 30
    ) -> Event:
        event = Event(
            name=name,
            description=description,
            organizer_name=organizer_name,
            organizer_email=organizer_email,
            passcode=passcode.strip() if passcode else None,
            retention_days=retention_days,
            status="active"
        )
        db.add(event)
        db.commit()
        db.refresh(event)
        return event

    @staticmethod
    def list_events(db: Session, status: str = "active") -> list[dict]:
        events = db.query(Event).filter(Event.status == status).order_by(Event.created_at.desc()).all()
        results = []
        for e in events:
            photo_count = db.query(Photo).filter(Photo.event_id == e.id).count()
            indexed_photos = db.query(Photo).filter(Photo.event_id == e.id, Photo.status == "indexed").count()
            results.append({
                "id": e.id,
                "name": e.name,
                "description": e.description,
                "organizer_name": e.organizer_name,
                "organizer_email": e.organizer_email,
                "has_passcode": bool(e.passcode),
                "retention_days": e.retention_days,
                "status": e.status,
                "created_at": e.created_at.isoformat(),
                "total_photos": photo_count,
                "indexed_photos": indexed_photos
            })
        return results

    @staticmethod
    def get_event(db: Session, event_id: str, passcode: str = None) -> Event | None:
        event = db.query(Event).filter(Event.id == event_id).first()
        if not event or event.status == "deleted":
            return None
        if event.passcode and event.passcode != passcode:
            raise PermissionError("Invalid passcode for this event.")
        return event

    @staticmethod
    def delete_event(db: Session, event_id: str) -> bool:
        event = db.query(Event).filter(Event.id == event_id).first()
        if not event:
            return False

        # 1. Clean up photos from physical storage
        photos = db.query(Photo).filter(Photo.event_id == event_id).all()
        for p in photos:
            try:
                p_path = Path(p.file_path)
                if p_path.exists():
                    p_path.unlink()
            except Exception as ex:
                print(f"Error removing file {p.file_path}: {ex}")

        # 2. Remove vector index
        vector_index_manager.remove_index(event_id)

        # 3. Mark or delete DB records
        db.delete(event)
        db.commit()
        return True

    @staticmethod
    def audit_retention_policies(db: Session) -> list[str]:
        """Identifies and purges events past their retention days."""
        now = datetime.utcnow()
        events = db.query(Event).filter(Event.status == "active").all()
        purged = []
        for e in events:
            expiration = e.created_at + timedelta(days=e.retention_days)
            if now > expiration:
                EventService.delete_event(db, e.id)
                purged.append(f"Purged expired event {e.name} (ID: {e.id})")
        return purged
