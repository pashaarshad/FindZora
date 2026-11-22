import os
import cv2
import numpy as np
from dataclasses import dataclass
from backend.face_engine.quality import assess_face_quality

@dataclass
class DetectedFace:
    bbox: tuple[int, int, int, int]  # (x, y, w, h)
    face_crop: np.ndarray             # BGR image crop
    aligned_crop: np.ndarray         # Normalized crop
    is_usable: bool
    quality_score: float
    blur_score: float
    filter_reason: str

class FaceDetector:
    def __init__(self):
        # Primary cascade: frontal face default
        cascade_path = os.path.join(cv2.data.haarcascades, "haarcascade_frontalface_default.xml")
        self.cascade = cv2.CascadeClassifier(cascade_path)

        # Fallback cascade: frontal face alt2 (better with glasses and slight angles)
        alt_path = os.path.join(cv2.data.haarcascades, "haarcascade_frontalface_alt2.xml")
        self.alt_cascade = cv2.CascadeClassifier(alt_path) if os.path.exists(alt_path) else None

    def detect_faces(self, image_bgr: np.ndarray, target_size=(112, 112)) -> list[DetectedFace]:
        """
        Detects multiple faces in an image, checks quality, and prepares normalized crops.
        Uses primary cascade with multi-scale tuning and alt cascade fallback.
        """
        if image_bgr is None or image_bgr.size == 0:
            return []

        h, w = image_bgr.shape[:2]
        gray = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2GRAY)
        gray_eq = cv2.equalizeHist(gray)

        # 1. Primary detection
        raw_faces = self.cascade.detectMultiScale(
            gray_eq,
            scaleFactor=1.08,
            minNeighbors=4,
            minSize=(30, 30),
            flags=cv2.CASCADE_SCALE_IMAGE
        )

        # 2. If no faces found, try alternate cascade
        if len(raw_faces) == 0 and self.alt_cascade is not None:
            raw_faces = self.alt_cascade.detectMultiScale(
                gray,
                scaleFactor=1.08,
                minNeighbors=3,
                minSize=(30, 30)
            )

        # 3. If still no faces found, check if image itself is already a tight face crop/portrait
        if len(raw_faces) == 0:
            # If aspect ratio is close to square or portrait, treat the central 80% as a face candidate
            usable, q, b, reason = assess_face_quality(image_bgr)
            if usable and w >= 50 and h >= 50:
                aligned = cv2.resize(image_bgr, target_size, interpolation=cv2.INTER_AREA)
                return [
                    DetectedFace(
                        bbox=(0, 0, w, h),
                        face_crop=image_bgr,
                        aligned_crop=aligned,
                        is_usable=True,
                        quality_score=q,
                        blur_score=b,
                        filter_reason="Full Portrait Crop"
                    )
                ]
            return []

        detected_faces = []
        for (x, y, bw, bh) in raw_faces:
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

_detector_instance = None

def get_face_detector() -> FaceDetector:
    global _detector_instance
    if _detector_instance is None:
        _detector_instance = FaceDetector()
    return _detector_instance
