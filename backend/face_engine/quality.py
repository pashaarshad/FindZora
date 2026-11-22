import cv2
import numpy as np
from backend.config import BLUR_THRESHOLD, MIN_FACE_SIZE

def assess_face_quality(face_crop: np.ndarray) -> tuple[bool, float, float, str]:
    """
    Assesses face image quality based on size, sharpness (Laplacian variance), and exposure.
    Returns:
        (is_usable: bool, quality_score: float [0..1], blur_score: float, reason: str)
    """
    if face_crop is None or face_crop.size == 0:
        return False, 0.0, 0.0, "Empty crop"

    h, w = face_crop.shape[:2]
    if h < MIN_FACE_SIZE or w < MIN_FACE_SIZE:
        return False, 0.2, 0.0, f"Face resolution too small ({w}x{h} < {MIN_FACE_SIZE}px)"

    # Convert to grayscale if color
    if len(face_crop.shape) == 3:
        gray = cv2.cvtColor(face_crop, cv2.COLOR_BGR2GRAY)
    else:
        gray = face_crop

    # Sharpness / Blur measurement via Laplacian variance
    lap_var = float(cv2.Laplacian(gray, cv2.CV_64F).var())

    if lap_var < BLUR_THRESHOLD:
        return False, 0.3, lap_var, f"Face too blurry (Laplacian variance {lap_var:.1f} < {BLUR_THRESHOLD})"

    # Brightness / Contrast check
    mean_val = float(np.mean(gray))
    if mean_val < 25.0:
        return False, 0.35, lap_var, "Face too dark / severely underexposed"
    if mean_val > 240.0:
        return False, 0.35, lap_var, "Face overexposed / washed out"

    # Normalized quality score
    sharpness_norm = min(1.0, lap_var / 300.0)
    size_norm = min(1.0, max(w, h) / 200.0)
    quality_score = round(float(0.5 * sharpness_norm + 0.5 * size_norm), 3)

    return True, quality_score, lap_var, "Acceptable"
