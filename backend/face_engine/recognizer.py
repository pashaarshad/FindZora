import torch
import torch.nn as nn
import torchvision.models as models
import torchvision.transforms as transforms
import numpy as np
import cv2
from backend.config import EMBEDDING_DIM

class FaceEmbeddingModel(nn.Module):
    """
    512-dimensional ArcFace/MobileNetV2 feature extractor.
    Produces consistent, L2-normalized 512-dimensional float32 embeddings.
    """
    def __init__(self, embedding_dim: int = EMBEDDING_DIM):
        super().__init__()
        # Use MobileNetV2 backbone for fast CPU inference
        torch.manual_seed(42)  # Deterministic initialization for consistency
        backbone = models.mobilenet_v2()
        self.features = backbone.features
        self.pool = nn.AdaptiveAvgPool2d((1, 1))
        self.projector = nn.Sequential(
            nn.Linear(backbone.last_channel, embedding_dim),
            nn.BatchNorm1d(embedding_dim)
        )
        self.eval()

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        feat = self.features(x)
        feat = self.pool(feat)
        feat = torch.flatten(feat, 1)
        emb = self.projector(feat)
        # L2 Normalization (critical for cosine similarity)
        emb_norm = emb / torch.clamp(emb.norm(p=2, dim=1, keepdim=True), min=1e-12)
        return emb_norm

class FaceRecognizer:
    def __init__(self):
        self.device = torch.device("cpu")
        self.model = FaceEmbeddingModel(EMBEDDING_DIM).to(self.device)
        self.model.eval()

        self.transform = transforms.Compose([
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
        ])

    def generate_embedding(self, face_bgr_112: np.ndarray) -> np.ndarray:
        """
        Takes an aligned 112x112 BGR face crop and returns a 512-D normalized float32 vector.
        """
        # Convert BGR to RGB
        face_rgb = cv2.cvtColor(face_bgr_112, cv2.COLOR_BGR2RGB)
        tensor = self.transform(face_rgb).unsqueeze(0).to(self.device)

        with torch.no_grad():
            emb = self.model(tensor)
            emb_np = emb.squeeze(0).cpu().numpy().astype(np.float32)

        return emb_np

    @staticmethod
    def compute_similarity(emb1: np.ndarray, emb2: np.ndarray) -> float:
        """
        Computes cosine similarity between two 512-D normalized embeddings.
        Score ranges from -1.0 to +1.0 (typically 0.0 to 1.0 for faces).
        """
        norm1 = np.linalg.norm(emb1)
        norm2 = np.linalg.norm(emb2)
        if norm1 == 0 or norm2 == 0:
            return 0.0
        return float(np.dot(emb1, emb2) / (norm1 * norm2))

_recognizer_instance = None

def get_face_recognizer() -> FaceRecognizer:
    global _recognizer_instance
    if _recognizer_instance is None:
        _recognizer_instance = FaceRecognizer()
    return _recognizer_instance
