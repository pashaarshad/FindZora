"""
FindZora Universal Folder Watcher CLI
Converts local or VPS folders into self-indexing event photo servers.

Folder Hierarchy:
universal_folder/
├── event_name_1/
│   ├── photo1.jpg
│   ├── photo2.jpg
│   └── face_clusters.json   # Maps Person IDs (e.g. 101) to photo paths & facial points
└── event_name_2/
    └── ...
"""

import os
import sys
import time
import json
import argparse
from pathlib import Path

# Add project root to path
ROOT_DIR = Path(__file__).resolve().parent.parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

import cv2
import numpy as np
from backend.face_engine.detector import get_face_detector
from backend.face_engine.recognizer import get_face_recognizer

UNIVERSAL_FOLDER_PATH = ROOT_DIR / "universal_folder"
SUPPORTED_EXTS = {".jpg", ".jpeg", ".png", ".webp"}

def extract_facial_points(face_crop: np.ndarray, bbox: tuple[int, int, int, int]) -> dict:
    """
    Extracts geometric facial landmark keypoints normalized for fast JSON storage & comparison.
    Points include: left_eye, right_eye, nose_tip, mouth_left, mouth_right, chin_center.
    """
    x, y, w, h = bbox
    # Approximate normalized 6-point geometry relative to face box
    return {
        "bbox": [int(x), int(y), int(w), int(h)],
        "landmarks": {
            "left_eye": [round(x + 0.3 * w, 1), round(y + 0.35 * h, 1)],
            "right_eye": [round(x + 0.7 * w, 1), round(y + 0.35 * h, 1)],
            "nose_tip": [round(x + 0.5 * w, 1), round(y + 0.55 * h, 1)],
            "mouth_left": [round(x + 0.35 * w, 1), round(y + 0.75 * h, 1)],
            "mouth_right": [round(x + 0.65 * w, 1), round(y + 0.75 * h, 1)],
            "chin_center": [round(x + 0.5 * w, 1), round(y + 0.95 * h, 1)]
        }
    }

def process_event_folder(event_dir: Path):
    """
    Scans an event folder, detects new photos, extracts facial points & embeddings,
    clusters people into IDs (101, 102, ...), and writes/updates face_clusters.json.
    """
    index_file = event_dir / "face_clusters.json"
    clusters_data = {
        "event_folder": event_dir.name,
        "last_updated": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "processed_files": {},
        "person_clusters": {}
    }

    if index_file.exists():
        try:
            with open(index_file, "r", encoding="utf-8") as f:
                clusters_data = json.load(f)
        except Exception as e:
            print(f"[{event_dir.name}] Warning: Could not read existing face_clusters.json: {e}")

    detector = get_face_detector()
    recognizer = get_face_recognizer()

    # Image files in folder
    image_files = [f for f in event_dir.iterdir() if f.is_file() and f.suffix.lower() in SUPPORTED_EXTS]
    new_processed = 0

    known_embeddings = []  # list of (person_id, embedding_vector)
    for pid, cdata in clusters_data.get("person_clusters", {}).items():
        if "representative_embedding" in cdata:
            known_embeddings.append((pid, np.array(cdata["representative_embedding"], dtype=np.float32)))

    for img_path in image_files:
        rel_name = img_path.name
        if rel_name in clusters_data.get("processed_files", {}):
            continue  # Already indexed

        img = cv2.imread(str(img_path))
        if img is None:
            continue

        detected_faces = detector.detect_faces(img)
        faces_info = []

        for df in detected_faces:
            if not df.is_usable:
                continue

            points = extract_facial_points(df.face_crop, df.bbox)
            emb = recognizer.generate_embedding(df.aligned_crop)

            # Compare against known person clusters (threshold 0.55)
            matched_person_id = None
            highest_sim = 0.0

            for pid, ref_emb in known_embeddings:
                sim = recognizer.compute_similarity(emb, ref_emb)
                if sim > highest_sim and sim >= 0.55:
                    highest_sim = sim
                    matched_person_id = pid

            if not matched_person_id:
                # Assign new Person ID (e.g. 101, 102...)
                cluster_nums = [int(p) for p in clusters_data["person_clusters"].keys() if p.isdigit()]
                next_id = str(max(cluster_nums) + 1 if cluster_nums else 101)
                matched_person_id = next_id
                clusters_data["person_clusters"][matched_person_id] = {
                    "person_id": matched_person_id,
                    "label": f"Person_{matched_person_id}",
                    "representative_embedding": [round(float(v), 5) for v in emb[:32]],  # sample for JSON
                    "total_photos": 0,
                    "photo_paths": []
                }
                known_embeddings.append((matched_person_id, emb))

            # Add photo path to person's cluster if not already present
            if rel_name not in clusters_data["person_clusters"][matched_person_id]["photo_paths"]:
                clusters_data["person_clusters"][matched_person_id]["photo_paths"].append(rel_name)
                clusters_data["person_clusters"][matched_person_id]["total_photos"] = len(
                    clusters_data["person_clusters"][matched_person_id]["photo_paths"]
                )

            faces_info.append({
                "person_id": matched_person_id,
                "bbox": points["bbox"],
                "landmarks": points["landmarks"],
                "quality_score": df.quality_score
            })

        clusters_data["processed_files"][rel_name] = {
            "faces_detected": len(faces_info),
            "faces": faces_info
        }
        new_processed += 1
        print(f"[{event_dir.name}] ✓ Processed {rel_name}: {len(faces_info)} face(s) mapped.")

    if new_processed > 0:
        clusters_data["last_updated"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        with open(index_file, "w", encoding="utf-8") as f:
            json.dump(clusters_data, f, indent=2)
        print(f"[{event_dir.name}] Saved updated index with {len(clusters_data['person_clusters'])} person cluster(s) -> {index_file.name}")

def run_watcher(watch_dir: Path, poll_interval: int = 3):
    print("=" * 60)
    print("  FindZora Universal Watch Folder CLI Server")
    print(f"  Watching: {watch_dir.resolve()}")
    print("  Status: Active | Press Ctrl+C to stop")
    print("=" * 60)

    watch_dir.mkdir(parents=True, exist_ok=True)

    while True:
        try:
            # Check all subfolders (each is an event)
            for event_dir in watch_dir.iterdir():
                if event_dir.is_dir() and not event_dir.name.startswith("."):
                    process_event_folder(event_dir)
            time.sleep(poll_interval)
        except KeyboardInterrupt:
            print("\n[FindZora Watcher] Stopped gracefully.")
            break
        except Exception as e:
            print(f"[FindZora Watcher] Error: {e}")
            time.sleep(poll_interval)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="FindZora Universal Watch Folder CLI")
    parser.add_argument("--dir", default=str(UNIVERSAL_FOLDER_PATH), help="Folder to watch")
    parser.add_argument("--scan-once", action="store_true", help="Scan once and exit")
    parser.add_argument("--interval", type=int, default=3, help="Polling interval in seconds")
    args = parser.parse_args()

    target_path = Path(args.dir)
    if args.scan_once:
        print(f"Scanning {target_path} once...")
        for ed in target_path.iterdir():
            if ed.is_dir():
                process_event_folder(ed)
        print("Done.")
    else:
        run_watcher(target_path, poll_interval=args.interval)
