import os
import cv2
import numpy as np
from dataclasses import dataclass
from backend.face_engine.quality import assess_face_quality

@dataclass
class DetectedFace:
    bbox: tuple[int, int, int, int]  # (x, y, w, h)
    face_crop: np.ndarray             # BGR image crop
    aligned_crop: np.ndarray         # Normalized 112x112 crop
    is_usable: bool
    quality_score: float
    blur_score: float
    filter_reason: str

class FaceDetector:
    def __init__(self):
        # Load OpenCV Haar cascade frontal face model
        cascade_path = os.path.join(cv2.data.haarcascades, "haarcascade_frontalface_default.xml")
        self.cascade = cv2.CascadeClassifier(cascade_path)
        if self.cascade.empty():
            raise RuntimeError(f"Failed to load Haar Cascade from {cascade_path}")

    def detect_faces(self, image_bgr: np.ndarray, target_size=(112, 112)) -> list[DetectedFace]:
        """
        Detects multiple faces in an image, checks quality, and prepares normalized crops.
        """
        if image_bgr is None or image_bgr.size == 0:
            return []

        h, w = image_bgr.shape[:2]
        gray = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2GRAY)
        # Contrast adjustment for better detection
        gray = cv2.equalizeHist(gray)

        # Multi-scale face detection
        raw_faces = self.cascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30),
            flags=cv2.CASCADE_SCALE_IMAGE
        )

        detected_faces = []
        for (x, y, bw, bh) in raw_faces:
            # Add small 10% context margin around face box
            pad_x = int(bw * 0.1)
            pad_y = int(bh * 0.1)
            x1 = max(0, x - pad_x)
            y1 = max(0, y - pad_y)
            x2 = min(w, x + bw + pad_x)
            y2 = min(h, y + bh + pad_y)

            crop = image_bgr[y1:y2, x1:x2]
            if crop.size == 0:
                continue

            is_usable, quality_score, blur_score, reason = assess_face_quality(crop)

            # Normalized aligned crop for embedding generator
            aligned = cv2.resize(crop, target_size, interpolation=cv2.INTER_AREA)

            detected_faces.append(
                DetectedFace(
                    bbox=(int(x), int(y), int(bw), int(bh)),
                    face_crop=crop,
                    aligned_crop=aligned,
                    is_usable=is_usable,
                    quality_score=quality_score,
                    blur_score=blur_score,
                    filter_reason=reason
                )
            )

        return detected_faces

# Singleton instance
_detector_instance = None

def get_face_detector() -> FaceDetector:
    global _detector_instance
    if _detector_instance is None:
        _detector_instance = FaceDetector()
    return _detector_instance
