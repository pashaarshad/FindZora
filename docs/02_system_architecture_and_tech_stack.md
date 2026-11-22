# FindZora: System Architecture & Recommended Tech Stack

5. System Architecture and Data Flow
The architecture separates the user-facing application, API, asynchronous processing workers, metadata database,
vector index and private image storage. The frontend and backend communicate bidirectionally through requests and
responses. The image-indexing pipeline is asynchronous and usually runs after upload, independently of an attendee's
search request.
5.1 Upload and indexing flow
G
Organiser uploads image → API validates user, event, file type, size and dimensions.
G
API stores the original image privately and creates a processing job.
G
Worker detects faces → applies quality checks → aligns each usable face → generates embeddings.
G
Worker saves face metadata and vectors; it marks the job processed, partially processed or failed.
G
Failed jobs can be retried without duplicating successful face records.
5.2 Search flow
G
Attendee opens an event link, reviews consent and captures a selfie.
G
API validates event access and capture constraints.
G
Recognition service detects and aligns the query face and generates its embedding.
G
Vector search is restricted to the selected event's index.
G
Backend applies calibrated thresholds, ranks candidate faces, deduplicates photo IDs and checks access
permissions.
G
Frontend displays authorised candidate photographs and provides a wrong-match/report option.
5.3 One server versus scalable deployment

A single laptop or server is acceptable for a controlled prototype. It is not a safe assumption for one lakh registered
users or thousands of simultaneous requests. In a larger deployment, run multiple stateless API instances behind a
load balancer, scale background workers separately, and use shared durable storage and a vector-search service.
Capacity must be sized from measured concurrency, event size, request rate and latency targets—not total registered
users alone.

8. Recommended Technology Stack and Repository
Layer
Prototype choice
Scale-up option
Frontend
Next.js + React
Next.js deployment with CDN and edge delivery where
appropriate
API
Python FastAPI
Multiple stateless API instances behind a load balancer
Image processing
OpenCV + Pillow
Optimised workers and GPU inference if justified
Face detector
Evaluate RetinaFace or another suitable detector
Benchmark detector options on event images
Recognition
Licensed ArcFace-compatible model
Model serving with version control and monitoring
Vector search
FAISS
Managed/distributed vector service if required
Metadata
SQLite for local prototype
PostgreSQL
Background jobs
Simple local worker initially
Redis + Celery or equivalent queue
Image storage
Private local folder
Private object storage with signed access
Deployment
One laptop on trusted LAN
Cloud or managed infrastructure
Suggested project structure
FindZora/
III frontend/ # Next.js + React
III backend/
I III api/ # FastAPI routes
I III face_engine/ # detection, alignment, embeddings
I III workers/ # asynchronous image processor
I III vector_index/ # FAISS index management
I III services/ # permissions, search, retention
I III tests/
III storage/ # private photos; never public web assets
III database/ # local development data
III docs/
III README.md
Keep event photographs, selfies, embeddings, credentials and database files out of GitHub. Never place private
photographs in the Next.js public directory. Use environment variables or a secrets manager for credentials. For phone
camera testing over local Wi-Fi, browsers generally require HTTPS for camera access, except localhost; use a trusted
local HTTPS setup rather than exposing the development server publicly.

