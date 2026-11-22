# FindZora: Research Roadmap & Demonstration Acceptance Criteria

12. Future Scope and Research Roadmap
Future research may extend FindZora beyond face-based matching into a multi-modal person re-identification system.
These are exploratory directions and are not part of the current working scope. They must be evaluated for reliability,
privacy, fairness and legal suitability before implementation.
12.1 Back-view and top-view research
The long-term research idea is to explore whether a person can sometimes be re-identified when the face is not
visible, using multiple visual cues. Possible cues include hair volume/quantity, hair colour, hairstyle, clothing colour
and type, body silhouette, pose, accessories, and scene or camera context. Top-view imagery may provide different
cues such as clothing layout, body outline and movement patterns.
Important limitation: hair and clothing are changeable, can be shared by many people and can be obscured. They are
not reliable substitutes for facial identity. A back-view or top-view model may produce candidate associations, not
guaranteed identity matches. The system must not claim 100% accuracy from these views.
12.2 Potential future modules
Research area
Potential direction
Caution
Multi-angle face matching
Improve matching across front, side and partial-profile
views.
Requires suitable data and model
evaluation.
Hair quantity / volume
Estimate broad hair-volume characteristics from visible
views.
Affected by hairstyle, lighting, headwear and
camera angle.
Hair colour
Use colour as a supporting visual cue.
Colour changes, lighting and image
processing can mislead.
Hairstyle recognition
Classify broad styles such as short, long, curly or tied.
Style changes and occlusion reduce
reliability.

Research area
Potential direction
Caution
Clothing attributes
Use colour, type or pattern as temporary contextual cues.
People change clothes; guests may wear
similar outfits.
Body silhouette and pose
Study shape and posture patterns in permitted images.
Pose, clothing and camera perspective
affect estimates.
Top-view analysis
Explore person association from overhead event footage.
Face often unavailable; evidence is weak
and context-specific.
Person re-identification
Combine face and non-face cues in a controlled
candidate-ranking model.
Must avoid treating visual similarity as
identity proof.
Privacy-preserving ML
Explore encrypted processing, on-device inference and
data minimisation.
Security and accuracy trade-offs require
independent review.
Advanced anti-spoofing
Evaluate presentation-attack detection and capture
integrity.
No method should be represented as
infallible.
12.3 Long-term vision
Evolve FindZora from an event-scoped face-search prototype into a privacy-preserving, context-aware event photo
discovery platform that can use multiple carefully evaluated visual signals when face evidence is unavailable. It should
continue to return candidate matches with uncertainty, keep event boundaries and consent central, and never promise
perfect identification.

13. Implementation Roadmap
A practical implementation sequence is to deliver a small, measurable MVP before attempting advanced features or
large-scale deployment.
Phase
Work
Deliverable
1. Foundation
Set up Next.js frontend, FastAPI backend, local database,
private storage and event model.
App skeleton and event creation.
2. Ingestion
Implement batch uploads, validation, queue/worker and
processing status.
Reliable upload and background job flow.
3. Recognition index
Integrate detector, quality gate, alignment, embedding model
and FAISS.
Event-specific precomputed index.
4. Attendee search
Consent flow, camera capture, query embedding, event-filtered
search and gallery.
End-to-end photo discovery.
5. Privacy and
reliability
Access control, retention/deletion, logs, retry, error handling and
incorrect-match reporting.
Safer MVP.
6. Evaluation
Build labelled test set; measure precision, recall, false matches
and latency.
Performance report and calibrated
threshold.
7. Scale-up
Load test, tune workers, evaluate PostgreSQL/object storage
and multi-instance APIs.
Evidence-based scale plan.
A seven-day demonstration schedule can produce a narrow prototype if the scope is tightly controlled and sample data
is ready. It should not be described as a production-ready biometric platform. A reliable production system needs more
time for evaluation, privacy review, security testing and operational hardening.

14. Demonstration Plan and Acceptance Criteria
Suggested demonstration
G
Organiser creates an event and uploads a small permissioned photo set.
G
Show the processing queue and status for uploaded images.
G
Open a group photo and show detected face boxes in a developer/admin view.
G
Show that face embeddings are indexed and linked to photo IDs, without exposing raw vectors to attendees.
G
Attendee selects the event, reads consent and captures a selfie.
G
Show the search request and event-scoped vector lookup.
G
Display ranked candidate photos and demonstrate a wrong-match report.
G
Show that a user cannot access another event or another attendee's restricted gallery.
G
Demonstrate retention/deletion or an administrator-controlled deletion request.
Acceptance criteria for the MVP
Area
Acceptance condition
Upload
Valid photos upload; invalid files are rejected with clear messages.
Processing
Jobs complete or fail visibly; retries do not create duplicate face records.
Detection
Multiple sufficiently clear faces can be detected and indexed in test images.
Search
Query searches only the selected event index.
Results
Candidate photos are ranked, deduplicated and access-checked.
Privacy
Consent, permissions and deletion workflow are demonstrable.
Evaluation
Precision, recall, false-positive rate and latency are reported on labelled test data.

