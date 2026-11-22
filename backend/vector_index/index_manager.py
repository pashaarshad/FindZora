import os
from pathlib import Path
import numpy as np
from dataclasses import dataclass
from backend.config import VECTOR_INDEX_DIR, EMBEDDING_DIM, SIMILARITY_THRESHOLD

@dataclass
class SearchCandidate:
    photo_id: str
    face_id: str
    similarity: float

class EventVectorIndex:
    """
    Manages fast vector similarity search for an individual event.
    Stores normalized 512-D float32 embeddings, face IDs, and photo IDs.
    Restricts search strictly to the isolated event index.
    """
    def __init__(self, event_id: str):
        self.event_id = event_id
        self.index_file = Path(VECTOR_INDEX_DIR) / f"{event_id}.npz"
        self.face_ids: list[str] = []
        self.photo_ids: list[str] = []
        self.embeddings: np.ndarray = np.empty((0, EMBEDDING_DIM), dtype=np.float32)
        self.load()

    def load(self):
        if self.index_file.exists():
            try:
                data = np.load(self.index_file)
                self.face_ids = list(data["face_ids"])
                self.photo_ids = list(data["photo_ids"])
                self.embeddings = data["embeddings"].astype(np.float32)
            except Exception as e:
                print(f"Error loading index for event {self.event_id}: {e}")

    def save(self):
        np.savez_compressed(
            self.index_file,
            face_ids=np.array(self.face_ids),
            photo_ids=np.array(self.photo_ids),
            embeddings=self.embeddings
        )

    def add_face(self, face_id: str, photo_id: str, embedding: np.ndarray):
        """
        Adds a single face embedding to the event index.
        """
        emb = embedding.astype(np.float32).reshape(1, EMBEDDING_DIM)
        # Normalize
        norm = np.linalg.norm(emb)
        if norm > 0:
            emb = emb / norm

        self.face_ids.append(face_id)
        self.photo_ids.append(photo_id)
        if self.embeddings.shape[0] == 0:
            self.embeddings = emb
        else:
            self.embeddings = np.vstack([self.embeddings, emb])

        self.save()

    def search(self, query_embedding: np.ndarray, top_k: int = 50, threshold: float = SIMILARITY_THRESHOLD) -> list[SearchCandidate]:
        """
        Performs cosine similarity search against indexed faces of this event.
        Returns ranked candidates above threshold, deduplicated by photo_id.
        """
        if self.embeddings.shape[0] == 0:
            return []

        q = query_embedding.astype(np.float32).reshape(1, EMBEDDING_DIM)
        q_norm = np.linalg.norm(q)
        if q_norm > 0:
            q = q / q_norm

        # Matrix dot product computes cosine similarities in parallel
        similarities = np.dot(self.embeddings, q.T).flatten()

        # Filter indices above threshold
        matched_indices = np.where(similarities >= threshold)[0]
        if len(matched_indices) == 0:
            return []

        # Sort descending by score
        sorted_matches = matched_indices[np.argsort(-similarities[matched_indices])]

        candidates: list[SearchCandidate] = []
        seen_photos: set[str] = set()

        for idx in sorted_matches:
            pid = self.photo_ids[idx]
            fid = self.face_ids[idx]
            sim = float(similarities[idx])

            # Deduplicate by photo ID (take highest confidence face per photo)
            if pid not in seen_photos:
                seen_photos.add(pid)
                candidates.append(SearchCandidate(photo_id=pid, face_id=fid, similarity=round(sim, 4)))
                if len(candidates) >= top_k:
                    break

        return candidates

    def delete_index(self):
        """Deletes this event's vector index from disk."""
        if self.index_file.exists():
            self.index_file.unlink()
        self.face_ids.clear()
        self.photo_ids.clear()
        self.embeddings = np.empty((0, EMBEDDING_DIM), dtype=np.float32)

class VectorIndexManager:
    def __init__(self):
        self._indices: dict[str, EventVectorIndex] = {}

    def get_index(self, event_id: str) -> EventVectorIndex:
        if event_id not in self._indices:
            self._indices[event_id] = EventVectorIndex(event_id)
        return self._indices[event_id]

    def remove_index(self, event_id: str):
        if event_id in self._indices:
            self._indices[event_id].delete_index()
            del self._indices[event_id]

vector_index_manager = VectorIndexManager()
