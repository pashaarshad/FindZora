# FindZora: AI-Powered Event Photo Discovery Platform

**Prepared by:** Arshad Pasha  
**Project Level:** Master of Computer Applications (MCA) — Version 2.0  
**Core Concept:** A consent-based, event-scoped photo discovery platform that indexes photographs once upon upload and searches the precomputed vector index when attendees request their photos using a camera verification selfie.

---

## 📁 Repository & System Structure (All in `FindZora`)

```text
FindZora/
├── app/                                      # Next.js / React App Router (Direct Root Frontend)
│   ├── page.tsx                              # Event discovery & event creation modal
│   ├── layout.tsx                            # Global layout with branding & navbar
│   ├── globals.css                           # Tailwind design tokens
│   ├── search/[eventId]/page.tsx             # Attendee selfie capture, consent & results gallery
│   └── organizer/page.tsx                    # Batch uploader, queue logs & bounding box viewer
│
├── components/                               # React UI Components
│   ├── Navbar.tsx                            # Header navigation
│   ├── ConsentModal.tsx                      # Biometric informed consent disclosure
│   ├── CameraCapture.tsx                     # WebRTC browser camera feed & snap tool
│   ├── CandidateGallery.tsx                  # Ranked candidate photos with match % & download
│   ├── BoundingBoxViewer.tsx                 # Interactive face detection overlay viewer
│   └── WrongMatchModal.tsx                   # Attendee wrong-match feedback dialogue
│
├── public/                                   # Frontend Static Assets
├── package.json                              # Next.js & React Dependencies & Scripts
├── tsconfig.json                             # TypeScript Configuration
├── tailwind.config.js                        # Tailwind CSS Configuration
├── postcss.config.js                         # PostCSS Configuration
├── next.config.mjs                           # Next.js Configuration with API Rewrites
│
├── backend/                                  # Python FastAPI High-Performance Backend
│   ├── api/                                  # Modular REST API Endpoints
│   │   ├── events.py                         # Event creation, listing, passcode & retention
│   │   ├── photos.py                         # Batch uploads, duplicate checks, streaming
│   │   ├── search.py                         # Attendee informed consent & selfie search
│   │   └── admin.py                          # Ingestion queue monitor, retry & wrong-match reports
│   ├── face_engine/                          # Biometric Computer Vision Pipeline
│   │   ├── detector.py                       # Multi-face detection & coordinate mapping
│   │   ├── quality.py                        # Quality gate (Laplacian blur variance & size checks)
│   │   └── recognizer.py                     # 512-D L2-normalized ArcFace/MobileNet embedding model
│   ├── workers/                              # Background Processing Worker
│   │   └── image_processor.py                # Asynchronous queue worker, retry & deduplication
│   ├── vector_index/                         # Isolated Event Vector Search Index
│   │   └── index_manager.py                  # Event-scoped cosine similarity matrix search
│   ├── services/                             # Business Logic Layer
│   │   ├── event_service.py                  # Event lifecycle & retention policy audit
│   │   ├── photo_service.py                  # SHA-256 duplicate validation & file storage
│   │   └── search_service.py                 # Ephemeral query processing & candidate ranking
│   ├── database/                             # Database Models & ORM
│   │   ├── connection.py                     # SQLite engine & session manager
│   │   └── models.py                         # Event, Photo, FaceRecord, Job, Consent & Report tables
│   ├── tests/                                # Automated Test Suite (pytest)
│   │   ├── test_face_engine.py               # Tests for quality assessment, 512-D norm & index
│   │   └── test_api.py                       # Tests for event lifecycle, consent & routes
│   ├── main.py                               # FastAPI application entrypoint with CORS
│   ├── config.py                             # Centralized system configurations
│   └── requirements.txt                      # Backend dependencies
│
├── All_Docs/                                 # Original Project Proposal & Documentation Templates
│   ├── FindZora_Final_Project_Documentation.pdf (5.2 MB Master Project Proposal)
│   ├── 01_executive_summary_and_features.md
│   ├── 02_system_architecture_and_tech_stack.md
│   ├── 03_recognition_pipeline_and_storage.md
│   ├── 04_privacy_security_and_limitations.md
│   ├── 05_roadmap_and_demonstration_plan.md
│   └── 06_viva_qa_and_glossary.md
│
├── docs/                                     # Extracted & Structured Engineering Documentation
│   ├── 01_executive_summary_and_features.md
│   ├── 02_system_architecture_and_tech_stack.md
│   ├── 03_recognition_pipeline_and_storage.md
│   ├── 04_privacy_security_and_limitations.md
│   ├── 05_roadmap_and_demonstration_plan.md
│   └── 06_viva_qa_and_glossary.md
│
├── storage/                                  # Private Secure Photo Storage
│   ├── photos/                               # Ingested high-res photographs (never exposed publicly)
│   └── temp/                                 # Ephemeral selfie captures (wiped immediately)
│
└── database/                                 # Local SQLite database files
    └── findzora.db
```

---

## 🚀 How to Run the Applications

### 1. Starting the Python FastAPI Backend

```bash
# In the FindZora root directory:
python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
```
- Interactive Swagger API Documentation: [http://localhost:8000/docs](http://localhost:8000/docs)
- Alternative Redoc Documentation: [http://localhost:8000/redoc](http://localhost:8000/redoc)

To run the automated test suite:
```bash
python -m pytest backend/tests -v
```

---

### 2. Starting the Next.js / React Frontend

```bash
# In the FindZora root directory:
npm install
npm run dev
```
Open your browser at [http://localhost:3000](http://localhost:3000).

---

## 🔒 Key Privacy & Architectural Guarantees

1. **Precomputed Indexing:** Event photographs are analyzed once during upload. Background workers detect faces, evaluate sharpness via Laplacian variance, and index 512-dimensional L2-normalized embeddings.
2. **Ephemeral Query Processing:** Attendee selfies captured via the browser camera are processed in memory to generate a query embedding and permanently deleted immediately afterwards.
3. **Event Isolation:** Biometric similarity searches are strictly bound to the requested `event_id`. Vector indices are isolated per event.
4. **Candidate Deduplication & Access Control:** High-resolution photos reside in private storage and are streamed only via authenticated endpoints; multiple face matches within one group photo return the photograph once.
5. **Wrong-Match Feedback:** Attendees can flag incorrect matches directly, enabling organizers to calibrate similarity thresholds.
