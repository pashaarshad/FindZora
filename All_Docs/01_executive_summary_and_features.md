# FindZora: Executive Summary, Problem Statement & Features

FindZora
AI-Powered Event Photo Discovery Platform
Final Project Proposal • System Architecture • Features • Limitations • Future Scope
Prepared by: Arshad Pasha
Project level: Master of Computer Applications (MCA)
Version 2.0 | 17 November 2026
A consent-based, event-scoped photo discovery system that indexes photographs once and
searches the prepared index when attendees request their photos.

1. Executive Summary
FindZora is a privacy-conscious event photo discovery platform for weddings, receptions, college functions, family
gatherings and other organised events. An authorised organiser or photographer uploads event photographs. The
system processes those photographs in the background, detects usable faces, generates numerical face embeddings
and stores searchable references. An attendee selects the relevant event, reads an informed-consent notice, captures
a selfie through the application and requests matching photographs. The backend generates an embedding for the
query selfie and searches only the selected event's index.
The central design principle is upload once, process once, index once, search many times. This avoids repeating
expensive face detection and embedding generation for every attendee search. The system still performs one
query-embedding operation for each search request; the saved index makes the comparison stage much faster.
FindZora is not a public face-search engine and does not establish a person's legal identity. It returns
probabilistic candidate matches for the attendee to review. It must not promise that every photograph
will be found or that recognition will be 100% accurate.
Project goals
G
Make it easier for attendees to find photographs in a large event collection.
G
Reduce repeated image processing by precomputing face embeddings during ingestion.
G
Support multiple faces in group photographs and event-specific searches.
G
Keep original images private and enforce event-level access permissions.
G
Measure accuracy, latency, storage and failure cases with a documented test dataset.
G
Start as a laptop-hosted prototype and evolve towards a horizontally scalable service.
Intended users
User role
Responsibility
Event organiser
Creates event, configures access, informs participants and controls retention.
Photographer / uploader
Uploads authorised event photographs and monitors processing.
Attendee
Gives informed consent, captures a selfie and views only permitted candidate results.
Administrator
Maintains accounts, infrastructure, security, backups and deletion workflows.

2. Problem Statement and Proposed Solution
At large events, hundreds or thousands of photographs may be captured by one or more photographers. Attendees
often need to browse large folders or contact the photographer to find images in which they appear. Group
photographs make manual searching even harder.
FindZora creates an event-scoped searchable collection. Each detected face is represented by a numerical
embedding linked to its photograph and event. A consenting attendee's query embedding is compared against the
relevant event index. The system returns ranked candidate photographs, not a guaranteed identity verdict.
Existing workflow versus FindZora
Traditional approach
FindZora approach
Manually browse folders and ask the photographer.
Select an event and search its indexed collection.
Repeatedly inspect original photos for each request.
Detect and index faces during background ingestion.
Sharing is often manual and inconsistent.
Provide an access-controlled candidate gallery.
Large collections become difficult to navigate.
Use event-scoped vector similarity search.
Scope boundary
G
The system searches only event collections for which the organiser has appropriate authority and participants have
been informed.
G
It does not search the open internet, identify strangers in public, or expose the full event gallery to every attendee.
G
It does not guarantee every appearance will be detected, especially when faces are hidden, tiny, blurred or turned
away.
G
A camera capture by itself does not prove liveness or prevent a person from presenting a photo or video to the
camera.

3. Core Ideas Finalised for FindZora
The following points combine the original project concept and the improvements proposed during planning.
3.1 Precomputed image processing
G
When an organiser uploads photographs, the system places them into a processing queue.
G
A Python background worker validates each image, detects multiple faces, checks face quality, aligns usable faces
and generates embeddings.
G
The worker stores embeddings and metadata once. The original photograph is stored once in private storage.
G
When an attendee searches, the backend generates an embedding from the attendee's consented selfie and
queries the prepared index.
G
The system does not rerun face detection and embedding generation over every original event photograph for
every search.
3.2 Multiple-face and group-photo support
G
Every sufficiently clear face detected in a group photo receives its own face record.
G
Each face record links back to the same original photo, so the gallery can return the photo once even if multiple
faces from it match.
G
Tiny, blurred or heavily occluded faces may be skipped or flagged rather than indexed as reliable records.
3.3 Attendee capture
G
Attendee selects the correct event and sees a clear consent notice.
G
Capture is through the browser camera in the intended flow; arbitrary gallery uploads are not part of the default
attendee search journey.
G
A front-facing capture and optional slight-angle captures may be supported.
G
The application should explain that multiple captures may help with pose variation but cannot guarantee a match.
3.4 Event isolation
G
Search is restricted to the selected event ID.
G
Event permissions are checked on the server for every search and image request.
G
No frontend client receives the complete vector index, raw embeddings or internal storage paths.

4. Features: Current Build, Recommended, and Later
This table distinguishes the features planned for the first working version from enhancements that can follow after the
core pipeline is reliable.
Feature
Status
Description
Event creation and organiser access
Core build
Create events, manage upload permissions and event access.
Batch photo upload
Core build
Upload supported image files with validation and progress.
Background processing
Core build
Queue images and process asynchronously, with retries.
Face detection
Core build
Detect multiple faces in individual and group photos.
Face quality filtering
Core build
Reject or flag unusable, tiny, blurry or heavily occluded faces.
Face alignment and embeddings
Core build
Align faces and generate consistent numerical embeddings.
FAISS similarity index
Core build
Search embeddings efficiently within the selected event.
Consent-based selfie capture
Core build
Capture query selfie through browser camera after notice and
consent.
Ranked candidate gallery
Core build
Return likely matching photos with conservative result handling.
Wrong-match reporting
Core build
Allow attendee to report a result that does not belong to them.
Private storage and access control
Core build
Protect original photos and return only authorised image references.
Processing dashboard
Recommended
Show uploaded, queued, processed, failed and skipped counts.
Multiple query captures
Recommended
Allow front and slight-angle reference captures.
Duplicate image detection
Recommended
Avoid repeated indexing of identical or near-identical uploads.
Retention and deletion dashboard
Recommended
Let organisers apply and audit event deletion policies.
Mobile app
Future enhancement
Native app experience after web prototype validation.
Advanced liveness / anti-spoofing
Future research
Evaluate presentation-attack detection; not guaranteed by camera
capture alone.
Multi-modal person re-identification
Future research
Combine face evidence with carefully governed visual cues.

