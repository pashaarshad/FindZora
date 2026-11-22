import uuid
from datetime import datetime
from sqlalchemy import Column, String, Integer, Float, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from backend.database.connection import Base

def generate_uuid():
    return str(uuid.uuid4())

class Event(Base):
    __tablename__ = "events"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    name = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    organizer_name = Column(String(100), nullable=False)
    organizer_email = Column(String(150), nullable=False)
    passcode = Column(String(50), nullable=True)  # Optional event access PIN
    retention_days = Column(Integer, default=30)
    status = Column(String(20), default="active")  # active, archived, deleted
    created_at = Column(DateTime, default=datetime.utcnow)

    photos = relationship("Photo", back_populates="event", cascade="all, delete-orphan")
    faces = relationship("FaceRecord", back_populates="event", cascade="all, delete-orphan")
    consent_logs = relationship("ConsentLog", back_populates="event", cascade="all, delete-orphan")
    wrong_reports = relationship("WrongMatchReport", back_populates="event", cascade="all, delete-orphan")

class Photo(Base):
    __tablename__ = "photos"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    event_id = Column(String(36), ForeignKey("events.id"), nullable=False, index=True)
    filename = Column(String(255), nullable=False)
    file_path = Column(String(500), nullable=False)
    file_hash = Column(String(64), nullable=False, index=True)  # SHA-256 for duplicate avoidance
    width = Column(Integer, default=0)
    height = Column(Integer, default=0)
    file_size = Column(Integer, default=0)
    status = Column(String(20), default="uploaded")  # uploaded, processing, indexed, failed
    face_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)

    event = relationship("Event", back_populates="photos")
    faces = relationship("FaceRecord", back_populates="photo", cascade="all, delete-orphan")
    processing_jobs = relationship("ProcessingJob", back_populates="photo", cascade="all, delete-orphan")

class FaceRecord(Base):
    __tablename__ = "face_records"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    photo_id = Column(String(36), ForeignKey("photos.id"), nullable=False, index=True)
    event_id = Column(String(36), ForeignKey("events.id"), nullable=False, index=True)
    bbox_x = Column(Integer, nullable=False)
    bbox_y = Column(Integer, nullable=False)
    bbox_w = Column(Integer, nullable=False)
    bbox_h = Column(Integer, nullable=False)
    quality_score = Column(Float, default=1.0)
    blur_score = Column(Float, default=100.0)
    model_version = Column(String(50), default="findzora_arcface_v1")
    created_at = Column(DateTime, default=datetime.utcnow)

    photo = relationship("Photo", back_populates="faces")
    event = relationship("Event", back_populates="faces")

class ProcessingJob(Base):
    __tablename__ = "processing_jobs"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    photo_id = Column(String(36), ForeignKey("photos.id"), nullable=False, index=True)
    event_id = Column(String(36), ForeignKey("events.id"), nullable=False, index=True)
    status = Column(String(20), default="queued")  # queued, processing, completed, failed
    attempts = Column(Integer, default=0)
    error_message = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    photo = relationship("Photo", back_populates="processing_jobs")

class ConsentLog(Base):
    __tablename__ = "consent_logs"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    event_id = Column(String(36), ForeignKey("events.id"), nullable=False, index=True)
    attendee_name = Column(String(100), nullable=True)
    consent_version = Column(String(50), default="v1.0")
    ip_hash = Column(String(64), nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)

    event = relationship("Event", back_populates="consent_logs")

class WrongMatchReport(Base):
    __tablename__ = "wrong_match_reports"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    event_id = Column(String(36), ForeignKey("events.id"), nullable=False, index=True)
    photo_id = Column(String(36), ForeignKey("photos.id"), nullable=False, index=True)
    attendee_notes = Column(Text, nullable=True)
    status = Column(String(30), default="pending_review")  # pending_review, confirmed_incorrect, dismissed
    created_at = Column(DateTime, default=datetime.utcnow)

    event = relationship("Event", back_populates="wrong_reports")
