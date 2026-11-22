# FindZora: Recognition Pipeline, Algorithm & Storage Strategy

6. Recognition Pipeline and Algorithm
6.1 Face detection is different from face recognition
Concept
Purpose in FindZora
Face detection
Finds face regions in an image.
Facial landmarks
Finds positions such as eyes, nose and mouth to help align the face.
Face alignment
Normalises face orientation and crop before embedding generation.
Face embedding
Converts a face crop into a numerical vector representing learned identity features.
Similarity search
Compares the query vector with indexed vectors to rank candidate matches.
The project should use a validated face-recognition model, such as an appropriately licensed ArcFace-compatible
model. OpenCV is useful for image handling and computer-vision operations, but OpenCV alone is not the
identity-recognition model. Model licensing and usage conditions must be checked before deployment.
6.2 Example embedding record
A face embedding may contain 512 floating-point values. The following is an illustrative shortened record, not a real
recognition output:
{"event_id":"event_001",
"photo_id":"photo_1024",
"face_id":"face_003",
"embedding":[0.124,-0.234,0.456,...],
"model_version":"model_v1"}
Do not store one separate giant JSON file per photograph as the production search mechanism. Use a database for
metadata and a vector index for embeddings. JSON can be used for export, debugging or interchange. The browser
should never download the complete index.
6.3 Similarity
Cosine similarity is commonly used to compare normalised embeddings: similarity = (A · B) / (||A|| × ||B||). The score is
a similarity measure, not a probability that two images show the same person. Thresholds must be calibrated on
representative data from the intended event conditions.
6.4 Consistency requirement
The same recognition model, model version, preprocessing, alignment method and normalisation must be used when
building the event index and when processing query selfies. Vectors from unrelated models generally cannot be
compared directly.

7. Storage, Performance and Scalability
The design reduces repeated computation, but it does not eliminate storage growth. Storage increases with original
image volume, number of detected faces, vector-index overhead, metadata, backups and retention duration.
7.1 Illustrative embedding storage
For a 512-dimensional embedding stored as 32-bit floats: 512 × 4 bytes = 2,048 bytes, approximately 2 KB per face
embedding. This is raw vector data only; real storage will be higher after metadata, indexes, database overhead and
replicas.
Indexed faces
Raw embedding estimate
1,000
~2 MB
10,000
~20 MB
100,000
~200 MB
1,000,000
~2 GB
10,000,000
~20 GB
7.2 Original photos may dominate storage
For example, 10,000 original photographs averaging 5 MB each require around 50 GB. If they contain 50,000 detected
faces, the raw 512-dimensional float32 embeddings require around 100 MB. The example demonstrates why image
storage and vector storage must be planned separately.
7.3 Storage optimisation
G
Store each original photograph once; link multiple face records to the same photo.
G
Detect duplicate uploads using file hashes and, where useful, perceptual hashes.
G
Use efficient binary vector storage rather than repeatedly parsing large JSON files.
G
Evaluate float16 or quantisation only after verifying that recognition quality remains acceptable.
G
Apply event-specific retention, archival and deletion policies.
G
Keep backups and replicas under explicit retention and access policies.
7.4 Performance and scaling
G
Use a background queue such as Redis + Celery for upload processing and retries.
G
Batch model inference where supported to use CPU/GPU resources efficiently.
G
Run multiple workers when indexing volume increases.
G
Use FAISS for the prototype; evaluate a managed or distributed vector database when scale and operations
require it.
G
Scale API servers and workers independently; keep API instances stateless where possible.
G
Cache safe, non-sensitive event metadata and use pagination for result galleries.
G
Measure p50/p95 latency, queue wait time, throughput, worker failure rate and storage growth.
A large number of registered users does not automatically mean the same number of simultaneous
searches. Design around measured concurrent requests and workload patterns.

