# FindZora: Privacy, Security, Evaluation & Limitations

9. Privacy, Security and Responsible Use
Face images and face embeddings are sensitive biometric information. Privacy is a core product requirement, not an
optional final feature.
Required safeguards
G
Provide a clear consent notice explaining the event, organiser, purpose, processing, retention, sharing and
limitations.
G
Obtain appropriate permission before uploading and processing event photographs; organisers must have
authority to use the images.
G
Provide a non-biometric alternative, such as requesting photos from the organiser or using an event/photo code.
G
Use guardian-led processes where children are involved and obtain appropriate consent.
G
Process attendee selfies temporarily and delete them after the search unless separate, explicit retention consent
exists.
G
Restrict every search and photo request to authorised event access; enforce permissions on the backend.
G
Use HTTPS, encryption at rest where appropriate, secure authentication, role-based access, rate limits and audit
logs.
G
Validate file type, size and image decoding; scan uploads and protect against malicious files.
G
Never expose raw embeddings, private storage paths, internal model files or unrestricted photo URLs to the
frontend.
G
Provide deletion, retention expiry, incident response and backup lifecycle processes.
Legal and governance note
Before any real-world deployment in India, review the Digital Personal Data Protection Act, 2023, applicable rules and
notifications in force at the time of launch, and obtain suitable legal advice. This document is a technical project
proposal, not a legal compliance certification.
Liveness limitation
Browser camera capture alone cannot prove that a live person is present. A person may hold up a photograph or play
a video to the camera. Advanced presentation-attack detection may be researched separately, but it also requires
evaluation and cannot be assumed to be perfect.

10. Accuracy, Testing and Evaluation
A promise of 100% accuracy is not technically responsible for a real-world face-recognition system. Accuracy depends
on image resolution, lighting, pose, occlusion, camera quality, age/time gaps, detector performance, model behaviour,
event conditions and the similarity threshold.
The correct project objective is to maximise measured performance, reduce false matches, document
limitations and make uncertain results safe to review.
10.1 Dataset plan
G
Create a permissioned test dataset with volunteers and documented consent.
G
Include individual and group photos, front and angled faces, indoor and outdoor lighting, different cameras and
realistic event conditions.
G
Include challenging examples such as blur, small faces, occlusion and partial profiles.
G
Keep a ground-truth record so that correct and incorrect matches can be measured.
G
Separate development and evaluation data; do not tune and report performance on the same examples only.
10.2 Metrics
Metric
Meaning
Precision
Of the returned matches, how many are correct?
Recall
Of all true matching photos, how many did the system find?
False-positive rate
How often does the system incorrectly match another person?
False-negative rate
How often does it fail to return a true match?
Search latency
How long does a query take, including queue/API/index time?
Throughput
How many searches or images can be handled per unit time?
10.3 Accuracy safeguards
G
Prioritise precision because showing an unrelated person's private photo is harmful.
G
Calibrate thresholds on representative event data; do not use a universal score cutoff.
G
Return ranked candidate results with an uncertainty message where appropriate.
G
Deduplicate results by photo ID and allow users to report incorrect matches.
G
Monitor performance across different lighting, poses and demographic groups where lawful and ethically
appropriate.
G
Do not use a high similarity score as proof of identity.

11. Limitations, Disadvantages and Not-in-Scope
Items
Limitation / disadvantage
Why it happens
Current handling
100% accuracy cannot be
promised
Real images vary and models can make errors.
Measure precision/recall; conservative
thresholds; user review.
Back-of-head identification is
not reliable with face recognition
No visible facial identity features.
Mark as unsupported in current version.
Top-view recognition is difficult
Face may be hidden or distorted by camera
angle.
Reject low-quality faces; future research only.
Tiny faces in group images may
be missed
Insufficient pixels for reliable detection and
identity features.
Quality gate and skip/flag.
Blur, poor lighting and occlusion
Important facial details are missing.
Quality checks and capture guidance.
Hair/clothing can change
Appearance cues are not stable identity proof.
Do not use as current identity matching basis.
Storage grows over time
Original images, embeddings, indexes and
backups accumulate.
Retention, deduplication, archival and scalable
storage.
High concurrent demand can
overload a single server
One host has finite CPU, memory, network and
disk capacity.
Queues, load balancing and horizontal scaling.
Camera capture is not liveness
proof
A photo/video may be presented to the camera.
Separate anti-spoofing research; honest
disclosure.
Model licensing and bias need
review
Models have usage terms and uneven
performance risks.
License review and representative testing.
Features explicitly not promised in the current version
G
Guaranteed identification from the back of the head or from a top-down view.
G
Guaranteed recognition through masks, helmets, heavy occlusion or very low-resolution faces.
G
Guaranteed 100% matching accuracy in every lighting or pose condition.
G
Automatic legal identity verification.
G
Public internet-wide person search or unrestricted cross-event search.
G
Perfect liveness detection from an ordinary browser camera.

