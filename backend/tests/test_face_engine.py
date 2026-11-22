import numpy as np
import cv2
from backend.face_engine.quality import assess_face_quality
from backend.face_engine.detector import get_face_detector
from backend.face_engine.recognizer import get_face_recognizer
from backend.vector_index.index_manager import EventVectorIndex

def test_face_quality_assessment():
    # Empty crop
    usable, q, b, reason = assess_face_quality(np.empty((0, 0, 3), dtype=np.uint8))
    assert not usable

    # Sharp synthetic face patch
    sharp_img = np.random.randint(50, 200, (112, 112, 3), dtype=np.uint8)
    usable, q, b, reason = assess_face_quality(sharp_img)
    assert usable
    assert q > 0

def test_recognizer_embedding_dimensions():
    rec = get_face_recognizer()
    crop = np.zeros((112, 112, 3), dtype=np.uint8)
    crop[30:80, 30:80] = 180  # synthetic shape
    emb = rec.generate_embedding(crop)
    assert emb.shape == (512,)
    # Check L2 normalization
    norm = np.linalg.norm(emb)
    assert np.isclose(norm, 1.0, atol=1e-3)

def test_vector_index_search():
    index = EventVectorIndex("test_event_99")
    emb1 = np.ones((512,), dtype=np.float32)
    emb1 = emb1 / np.linalg.norm(emb1)

    index.add_face(face_id="face_1", photo_id="photo_1", embedding=emb1)

    # Search with identical vector
    candidates = index.search(emb1, threshold=0.5)
    assert len(candidates) == 1
    assert candidates[0].photo_id == "photo_1"
    assert np.isclose(candidates[0].similarity, 1.0, atol=1e-3)

    # Clean up test index
    index.delete_index()
