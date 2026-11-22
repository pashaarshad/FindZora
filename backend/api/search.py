from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, Request
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
from backend.database.connection import get_db
from backend.services.search_service import SearchService
from backend.config import SIMILARITY_THRESHOLD

router = APIRouter(prefix="/api/events/{event_id}", tags=["Attendee Search"])

class ConsentRequest(BaseModel):
    attendee_name: Optional[str] = "Anonymous Attendee"

class WrongMatchRequest(BaseModel):
    photo_id: str
    attendee_notes: Optional[str] = "Photo does not match my face"

@router.post("/consent")
def record_attendee_consent(
    event_id: str,
    req: ConsentRequest,
    request: Request,
    db: Session = Depends(get_db)
):
    client_ip = request.client.host if request.client else "127.0.0.1"
    consent = SearchService.record_consent(
        db=db,
        event_id=event_id,
        attendee_name=req.attendee_name,
        client_ip=client_ip
    )
    return {
        "status": "consent_recorded",
        "consent_id": consent.id,
        "timestamp": consent.timestamp.isoformat()
    }

@router.post("/search")
async def search_event_photos(
    event_id: str,
    selfie: UploadFile = File(...),
    threshold: Optional[float] = Form(SIMILARITY_THRESHOLD),
    top_k: Optional[int] = Form(50),
    db: Session = Depends(get_db)
):
    content = await selfie.read()
    if not content:
        raise HTTPException(status_code=400, detail="Empty selfie file received.")

    result = SearchService.search_by_selfie(
        db=db,
        event_id=event_id,
        selfie_bytes=content,
        threshold=threshold or SIMILARITY_THRESHOLD,
        top_k=top_k or 50
    )
    return result

@router.post("/report-wrong-match")
def report_wrong_match(
    event_id: str,
    req: WrongMatchRequest,
    db: Session = Depends(get_db)
):
    report = SearchService.submit_wrong_match_report(
        db=db,
        event_id=event_id,
        photo_id=req.photo_id,
        attendee_notes=req.attendee_notes
    )
    return {
        "status": "report_submitted",
        "report_id": report.id,
        "message": "Thank you. Your feedback helps calibrate accuracy and protect privacy."
    }

universal_router = APIRouter(prefix="/api/search", tags=["Universal Search"])

@universal_router.post("/universal")
async def universal_search(
    selfie: UploadFile = File(...),
    threshold: Optional[float] = Form(SIMILARITY_THRESHOLD),
    db: Session = Depends(get_db)
):
    content = await selfie.read()
    if not content:
        raise HTTPException(status_code=400, detail="Empty selfie file received.")

    result = SearchService.search_universal_by_selfie(
        db=db,
        selfie_bytes=content,
        threshold=threshold or SIMILARITY_THRESHOLD
    )
    return result
