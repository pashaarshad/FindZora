from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
from backend.database.connection import get_db
from backend.services.event_service import EventService

router = APIRouter(prefix="/api/events", tags=["Events"])

class CreateEventRequest(BaseModel):
    name: str
    description: Optional[str] = ""
    organizer_name: str
    organizer_email: str
    passcode: Optional[str] = None
    retention_days: Optional[int] = 30

@router.post("", status_code=201)
def create_event(req: CreateEventRequest, db: Session = Depends(get_db)):
    event = EventService.create_event(
        db=db,
        name=req.name,
        organizer_name=req.organizer_name,
        organizer_email=req.organizer_email,
        description=req.description,
        passcode=req.passcode,
        retention_days=req.retention_days or 30
    )
    return {
        "id": event.id,
        "name": event.name,
        "organizer_name": event.organizer_name,
        "retention_days": event.retention_days,
        "created_at": event.created_at.isoformat()
    }

@router.get("")
def list_events(db: Session = Depends(get_db)):
    return EventService.list_events(db)

@router.get("/{event_id}")
def get_event(event_id: str, passcode: Optional[str] = Query(None), db: Session = Depends(get_db)):
    try:
        event = EventService.get_event(db, event_id, passcode)
        if not event:
            raise HTTPException(status_code=404, detail="Event not found")
        return {
            "id": event.id,
            "name": event.name,
            "description": event.description,
            "organizer_name": event.organizer_name,
            "organizer_email": event.organizer_email,
            "has_passcode": bool(event.passcode),
            "retention_days": event.retention_days,
            "created_at": event.created_at.isoformat()
        }
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))

@router.delete("/{event_id}")
def delete_event(event_id: str, db: Session = Depends(get_db)):
    success = EventService.delete_event(db, event_id)
    if not success:
        raise HTTPException(status_code=404, detail="Event not found")
    return {"message": f"Event {event_id} and all associated photos and vectors deleted."}

@router.post("/audit-retention")
def audit_retention(db: Session = Depends(get_db)):
    purged = EventService.audit_retention_policies(db)
    return {"status": "ok", "purged_events": purged}
