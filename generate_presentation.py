import os
import sys
from pathlib import Path
import pptx
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from pptx.dml.color import RGBColor

# -------------------------------------------------------------
# Color Palette - Clean, Light, Professional (Human-Crafted Feel)
# -------------------------------------------------------------
BG_COLOR = RGBColor(248, 250, 252)       # Slate 50 (#F8FAFC)
WHITE = RGBColor(255, 255, 255)          # Card background
CARD_BORDER = RGBColor(226, 232, 240)    # Slate 200 border
PRIMARY = RGBColor(2, 132, 199)          # Sky 600 (#0284C7)
PRIMARY_DARK = RGBColor(3, 105, 161)     # Sky 700 (#0369A1)
INDIGO = RGBColor(79, 70, 229)           # Indigo 600 (#4F46E5)
EMERALD = RGBColor(5, 150, 105)          # Emerald 600 (#059669)
AMBER = RGBColor(217, 119, 6)            # Amber 600 (#D97706)
TEXT_DARK = RGBColor(15, 23, 42)         # Slate 900
TEXT_BODY = RGBColor(51, 65, 85)         # Slate 700
TEXT_MUTED = RGBColor(100, 116, 139)     # Slate 500
PILL_BG = RGBColor(224, 242, 254)        # Sky 100

def set_slide_background(slide):
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = BG_COLOR

def add_header(slide, category: str, title: str, subtitle: str = None):
    # Category Pill
    pill = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(0.4), Inches(2.8), Inches(0.35))
    pill.fill.solid()
    pill.fill.fore_color.rgb = PILL_BG
    pill.line.color.rgb = RGBColor(186, 230, 253)
    pill.line.width = Pt(1)
    tf = pill.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = category.upper()
    p.alignment = PP_ALIGN.CENTER
    p.font.name = "Arial"
    p.font.size = Pt(10)
    p.font.bold = True
    p.font.color.rgb = PRIMARY_DARK

    # Top Right Corner Logo Icon
    icon_img = os.path.join(os.path.dirname(__file__), "public", "images", "findzora_icon.png")
    if os.path.exists(icon_img):
        slide.shapes.add_picture(icon_img, Inches(12.0), Inches(0.35), width=Inches(0.55))

    # Title
    tb = slide.shapes.add_textbox(Inches(0.8), Inches(0.8), Inches(11.7), Inches(0.6))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
    p = tf.paragraphs[0]
    p.text = title
    p.font.name = "Arial"
    p.font.size = Pt(22)
    p.font.bold = True
    p.font.color.rgb = TEXT_DARK

    # Subtitle
    if subtitle:
        tb_sub = slide.shapes.add_textbox(Inches(0.8), Inches(1.4), Inches(11.7), Inches(0.4))
        tf_sub = tb_sub.text_frame
        tf_sub.word_wrap = True
        tf_sub.margin_left = tf_sub.margin_top = tf_sub.margin_right = tf_sub.margin_bottom = 0
        p_sub = tf_sub.paragraphs[0]
        p_sub.text = subtitle
        p_sub.font.name = "Arial"
        p_sub.font.size = Pt(12)
        p_sub.font.color.rgb = TEXT_MUTED

def add_card(slide, left, top, width, height, title: str = None, items: list = None, header_color = PRIMARY):
    shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    shape.fill.solid()
    shape.fill.fore_color.rgb = WHITE
    shape.line.color.rgb = CARD_BORDER
    shape.line.width = Pt(1.2)

    tf = shape.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = MSO_ANCHOR.TOP
    tf.margin_left = Inches(0.25)
    tf.margin_top = Inches(0.22)
    tf.margin_right = Inches(0.25)
    tf.margin_bottom = Inches(0.2)

    first = True
    if title:
        p = tf.paragraphs[0]
        p.text = title
        p.font.name = "Arial"
        p.font.size = Pt(14)
        p.font.bold = True
        p.font.color.rgb = header_color
        p.space_after = Pt(8)
        first = False

    if items:
        for it in items:
            p = tf.add_paragraph() if not first else tf.paragraphs[0]
            first = False
            p.text = "• " + it if not it.startswith("•") else it
            p.font.name = "Arial"
            p.font.size = Pt(11)
            p.font.color.rgb = TEXT_BODY
            p.space_after = Pt(5)

    return shape

def create_presentation():
    prs = pptx.Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # =========================================================
    # SLIDE 1: Title Slide (Presenter: Mohammad Arsh)
    # =========================================================
    s1 = prs.slides.add_slide(blank_layout)
    set_slide_background(s1)

    # Main Card
    card = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.5), Inches(1.0), Inches(10.333), Inches(5.5))
    card.fill.solid()
    card.fill.fore_color.rgb = WHITE
    card.line.color.rgb = CARD_BORDER
    card.line.width = Pt(1.5)

    logo_img = os.path.join(os.path.dirname(__file__), "public", "images", "findzora_logo.png")
    if os.path.exists(logo_img):
        s1.shapes.add_picture(logo_img, Inches(2.2), Inches(1.35), width=Inches(3.4))

    tf = card.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    tf.margin_left = Inches(0.8)
    tf.margin_right = Inches(0.8)

    # Empty paragraph to leave space for the logo picture above
    p = tf.paragraphs[0]
    p.text = ""
    p.space_after = Pt(45)

    # Subtitle
    p2 = tf.add_paragraph()
    p2.text = "AI-Powered Event Photo Discovery Platform"
    p2.font.name = "Arial"
    p2.font.size = Pt(22)
    p2.font.bold = True
    p2.font.color.rgb = TEXT_DARK
    p2.space_after = Pt(14)

    # Tagline / Description
    p3 = tf.add_paragraph()
    p3.text = "A consent-based, event-scoped photo discovery system with precomputed biometric indexing, universal multi-event grouping, and autonomous watch folder CLI ingestion."
    p3.font.name = "Arial"
    p3.font.size = Pt(13)
    p3.font.color.rgb = TEXT_MUTED
    p3.space_after = Pt(36)

    # Presenter Information - Specifically: Mohammad Arsh
    p4 = tf.add_paragraph()
    p4.text = "Project Presenter:  Mohammad Arsh"
    p4.font.name = "Arial"
    p4.font.size = Pt(16)
    p4.font.bold = True
    p4.font.color.rgb = INDIGO
    p4.space_after = Pt(6)

    p5 = tf.add_paragraph()
    p5.text = "Master of Computer Applications (MCA) Project  |  Version 2.0"
    p5.font.name = "Arial"
    p5.font.size = Pt(12)
    p5.font.color.rgb = TEXT_MUTED

    # =========================================================
    # SLIDE 2: Problem Statement & Why It Matters
    # =========================================================
    s2 = prs.slides.add_slide(blank_layout)
    set_slide_background(s2)
    add_header(s2, "Problem Statement", "The Event Photo Dilemma & Real-World Friction",
               "Why traditional photo sharing at weddings, college convocations, and large gatherings is broken.")

    col_w = Inches(5.6)
    col_h = Inches(2.3)
    top1 = Inches(2.0)
    top2 = Inches(4.6)

    add_card(s2, Inches(0.8), top1, col_w, col_h, "1. Endless Manual Browsing Fatigue", [
        "Photographers capture 2,000 to 5,000+ high-res photos per event.",
        "Guests are forced to manually scroll through massive Google Drive / Dropbox dumps.",
        "Over 80% of attendees abandon searching before finding their candid moments."
    ], PRIMARY)

    add_card(s2, Inches(6.8), top1, col_w, col_h, "2. The Group Photograph Challenge", [
        "Manual face-tagging cannot easily identify individual faces in crowded group shots.",
        "A guest might be in the background of 15 group photos and never find them.",
        "Valuable candid memories remain permanently buried."
    ], INDIGO)

    add_card(s2, Inches(0.8), top2, col_w, col_h, "3. Overwhelming Photographer Workload", [
        "Photographers waste hours answering WhatsApp and email requests: 'Can you send my photos?'",
        "Repeated manual sorting and filtering delays client delivery by weeks.",
        "Need for an automated, zero-touch ingestion pipeline."
    ], AMBER)

    add_card(s2, Inches(6.8), top2, col_w, col_h, "4. The Privacy & Consent Deficit", [
        "Public dump links expose all photos to everyone, violating guest privacy.",
        "Traditional face apps harvest biometric data without informed consent.",
        "FindZora enforces event isolation and ephemeral selfie processing."
    ], EMERALD)

    # =========================================================
    # SLIDE 3: Proposed Solution - The FindZora Concept
    # =========================================================
    s3 = prs.slides.add_slide(blank_layout)
    set_slide_background(s3)
    add_header(s3, "Proposed Solution", "FindZora: Intelligent Precomputed Event Discovery",
               "A privacy-conscious, event-isolated platform indexing photos once and searching in milliseconds.")

    add_card(s3, Inches(0.8), Inches(2.0), Inches(3.6), Inches(4.8), "Precomputed Indexing", [
        "Photos are analyzed once upon upload.",
        "Multi-face detection locates every face.",
        "512-D L2-normalized embeddings generated.",
        "Embeddings and metadata stored permanently in FAISS / vector index.",
        "Zero redundant face processing during guest queries."
    ], PRIMARY)

    add_card(s3, Inches(4.8), Inches(2.0), Inches(3.6), Inches(4.8), "Ephemeral Selfie Query", [
        "Guest captures a single verification selfie via browser WebRTC camera.",
        "Informed biometric consent collected first.",
        "Query embedding generated in memory.",
        "Selfie photo is permanently deleted immediately after vector extraction.",
        "No raw vectors or private paths exposed."
    ], INDIGO)

    add_card(s3, Inches(8.8), Inches(2.0), Inches(3.6), Inches(4.8), "Multi-Event Grouping", [
        "Single selfie searches across all attended events.",
        "Photos grouped by event (Wedding, Convocation, etc.).",
        "One-click batch download button for each event.",
        "Individual photo tap for full-res view.",
        "Attendee feedback loop for wrong-match reporting."
    ], EMERALD)

    # =========================================================
    # SLIDE 4: Complete 18-Step Workflow (Infographic Diagram)
    # =========================================================
    s4 = prs.slides.add_slide(blank_layout)
    set_slide_background(s4)
    add_header(s4, "System Workflow", "Complete A-to-Z Operational Flow (18 Steps)",
               "From studio ingestion and precomputed AI indexing to guest camera discovery.")

    # Embed Infographic Image
    img_path = Path("public/images/findzora_workflow_infographic.jpg")
    if img_path.exists():
        s4.shapes.add_picture(str(img_path), Inches(0.8), Inches(2.0), width=Inches(8.2))

    # Right-side Stage Breakdown Card
    add_card(s4, Inches(9.2), Inches(2.0), Inches(3.3), Inches(4.8), "Workflow Stages", [
        "Stage 1: Organizer Portal (Steps 1–5)",
        "• Studio login & event creation",
        "• QR code & guest link distribution",
        "• Ingestion via Web or Watch Folder CLI",
        "",
        "Stage 2: AI Face Engine (Steps 6–10)",
        "• Multi-face detection & quality filter",
        "• 512-D ArcFace vector extraction",
        "• Event-isolated FAISS indexing",
        "",
        "Stage 3: Guest Discovery (Steps 11–18)",
        "• WebRTC camera selfie capture",
        "• Sub-second cosine similarity search",
        "• Grouped gallery & 1-click batch download",
        "• Wrong-match feedback & auto-retention"
    ], PRIMARY_DARK)

    # =========================================================
    # SLIDE 5: Recognition Pipeline & Algorithms
    # =========================================================
    s5 = prs.slides.add_slide(blank_layout)
    set_slide_background(s5)
    add_header(s5, "Core Algorithms", "Computer Vision Pipeline & Mathematical Models",
               "Multi-stage pipeline: Detection -> Quality Gate -> Alignment -> 512-D Embedding -> Cosine Match.")

    col3_w = Inches(3.6)
    add_card(s5, Inches(0.8), Inches(2.0), col3_w, Inches(2.4), "1. Face Detection & BBox", [
        "Algorithm: Haar Cascade & Deep SSD CNN.",
        "Multi-scale detection across varied face sizes.",
        "Identifies multiple faces in crowd & group shots.",
        "Outputs precise bounding box (x, y, w, h)."
    ], PRIMARY)

    add_card(s5, Inches(4.8), Inches(2.0), col3_w, Inches(2.4), "2. Face Quality Filter", [
        "Laplacian Blur Variance: Var(Laplacian) < 35.0 rejected.",
        "Minimum Resolution Gate: Faces < 40x40 px skipped.",
        "Brightness Check: Mean grayscale between 25 and 240.",
        "Prevents false positives from blurry background faces."
    ], INDIGO)

    add_card(s5, Inches(8.8), Inches(2.0), col3_w, Inches(2.4), "3. Landmark Alignment", [
        "Extracts 6 geometric facial landmarks:",
        "Left/right eyes, nose tip, mouth corners, chin.",
        "Normalizes affine orientation and crop.",
        "Standardizes face patch to 112x112 canonical size."
    ], EMERALD)

    add_card(s5, Inches(0.8), Inches(4.7), col3_w, Inches(2.2), "4. 512-D ArcFace Embedding", [
        "Backbone: Deep Convolutional Neural Network.",
        "Converts 112x112 crop into 512 float32 values.",
        "L2 Normalization: ||v|| = 1.0 (Unit hypersphere).",
        "High inter-class variance, low intra-class variance."
    ], PRIMARY_DARK)

    add_card(s5, Inches(4.8), Inches(4.7), Inches(7.6), Inches(2.2), "5. Vector Similarity Search & Calibration", [
        "Mathematical Formula: Cosine Similarity = (A · B) / (||A|| × ||B||) = A · B (since normalized).",
        "Search Speed: Matrix dot product computes 50,000+ comparisons in under 15 milliseconds.",
        "Calibrated Threshold: Conservative cutoff at 0.55 similarity (~97.5%+ confidence match).",
        "Deduplication: Takes highest confidence face per photo to avoid duplicate returns."
    ], AMBER)

    # =========================================================
    # SLIDE 6: Dataset & Database Architecture
    # =========================================================
    s6 = prs.slides.add_slide(blank_layout)
    set_slide_background(s6)
    add_header(s6, "Data Architecture", "Primary Dataset Plan & Storage Strategy",
               "Separating raw photo storage from lightweight vector indices for maximum scalability.")

    add_card(s6, Inches(0.8), Inches(2.0), Inches(5.6), Inches(4.8), "Primary / Custom Dataset Plan", [
        "Objective: Build an empirical primary dataset under documented volunteer consent.",
        "",
        "Dataset Composition & Diversity:",
        "• Real wedding, reception, and college convocation settings.",
        "• Varied camera hardware: DSLR, mirrorless, smartphone cameras.",
        "• Lighting conditions: Indoor warm event halls, direct sunlight, low light.",
        "• Challenging poses: Frontal, 45-degree angled, laughter, sunglasses/occlusion.",
        "",
        "Ground-Truth Benchmarking:",
        "• Manual identity labeling for test partitions.",
        "• Rigorous measurement of Precision, Recall, and False Match Rate (FMR).",
        "• Threshold calibration based on empirical ROC curves."
    ], PRIMARY)

    add_card(s6, Inches(6.8), Inches(2.0), Inches(5.6), Inches(2.3), "Relational Metadata (SQLite)", [
        "Events: ID, name, passcode, organizer credentials, retention days.",
        "Photos: ID, event_id, file_path, SHA-256 hash (duplicate detection).",
        "FaceRecords: ID, photo_id, bbox, quality_score, blur_score.",
        "ProcessingJobs: Queue status (queued, processing, completed, failed).",
        "ConsentLogs & WrongMatchReports for audit & compliance."
    ], INDIGO)

    add_card(s6, Inches(6.8), Inches(4.5), Inches(5.6), Inches(2.3), "Vector Storage & Scalability", [
        "Binary Compressed Index: NumPy / FAISS (.npz / .bin) per event.",
        "Raw vectors: 512 floats x 4 bytes = ~2 KB per face.",
        "50,000 faces require only ~100 MB vector storage.",
        "10,000 original photos require ~50 GB private storage.",
        "Event Isolation: Index files are partitioned strictly per event ID."
    ], EMERALD)

    # =========================================================
    # SLIDE 7: Universal Watch Folder CLI Architecture
    # =========================================================
    s7 = prs.slides.add_slide(blank_layout)
    set_slide_background(s7)
    add_header(s7, "Ingestion Innovation", "Universal Watch Folder: Zero-Touch Ingestion CLI",
               "Converting local or VPS folders into self-indexing event servers without web uploads.")

    add_card(s7, Inches(0.8), Inches(2.0), Inches(5.6), Inches(4.8), "How the Watch Folder Works", [
        "Photographers do NOT need to upload files via the web dashboard.",
        "",
        "1. Folder Structure on Local PC or VPS:",
        "   universal_folder/",
        "   ├── wedding_event_1/",
        "   │   ├── photo_01.jpg, photo_02.jpg ...",
        "   │   └── face_clusters.json",
        "   └── mca_convocation_2026/",
        "",
        "2. Automated Background Daemon (backend/cli/watch_folder.py):",
        "   • Polls every 3 seconds for new JPG/PNG files.",
        "   • Ingests photos directly from SD card sync or camera Wi-Fi dumps.",
        "   • Detects faces and computes facial landmark coordinates.",
        "   • Clusters individuals by Person ID (e.g. 101, 102 like Arshad)."
    ], PRIMARY)

    add_card(s7, Inches(6.8), Inches(2.0), Inches(5.6), Inches(4.8), "Generated JSON Cluster Format (face_clusters.json)", [
        "{\n  \"event_folder\": \"wedding_event_1\",\n  \"last_updated\": \"2026-11-22T19:35:00Z\",\n  \"person_clusters\": {\n    \"101\": {\n      \"person_id\": \"101\",\n      \"label\": \"Person_101 (Arshad)\",\n      \"total_photos\": 2,\n      \"photo_paths\": [\n        \"wedding_stage_01.jpg\",\n        \"candid_dinner_04.jpg\"\n      ]\n    },\n    \"102\": {\n      \"person_id\": \"102\",\n      \"total_photos\": 1,\n      \"photo_paths\": [\"wedding_stage_01.jpg\"]\n    }\n  }\n}",
        "",
        "Instant Guest Search:",
        "When an attendee queries, the system checks precomputed clusters in milliseconds with zero lag!"
    ], INDIGO)

    # =========================================================
    # SLIDE 8: Universal Multi-Event Attendee Discovery
    # =========================================================
    s8 = prs.slides.add_slide(blank_layout)
    set_slide_background(s8)
    add_header(s8, "Guest Experience", "Universal Multi-Event Grouping & 1-Click Downloads",
               "Discovering all attended events with a single selfie and seamless batch retrieval.")

    add_card(s8, Inches(0.8), Inches(2.0), Inches(3.6), Inches(4.8), "1. Unified Selfie Search", [
        "Single Verification Scan:",
        "The guest snaps one selfie on the FindZora home page.",
        "",
        "Cross-Event Query:",
        "FindZora matches the query vector across all events the person attended.",
        "",
        "Zero Redundant Work:",
        "No need to re-scan for each event separately."
    ], PRIMARY)

    add_card(s8, Inches(4.8), Inches(2.0), Inches(3.6), Inches(4.8), "2. Event-by-Event Grouping", [
        "Categorized Presentation:",
        "Photos are neatly grouped by event cards:",
        "• Event 1: Wedding Event 1 (4 Photos)",
        "• Event 2: MCA Convocation 2026 (6 Photos)",
        "• Event 3: Tech Innovations Summit (2 Photos)",
        "",
        "Confidence Badges:",
        "Each photo displays match confidence (e.g. 98.6% Match)."
    ], INDIGO)

    add_card(s8, Inches(8.8), Inches(2.0), Inches(3.6), Inches(4.8), "3. One-Click Batch Download", [
        "Dedicated Event Download:",
        "A single button: 'Download All Event Photos (ZIP)' per event.",
        "",
        "Individual Photo Inspection:",
        "• Tap any photo to open full-res lightbox.",
        "• Individual download & WhatsApp sharing.",
        "• 'Report Wrong Match' interactive feedback tool."
    ], EMERALD)

    # =========================================================
    # SLIDE 9: Technology Stack & Technical Justification
    # =========================================================
    s9 = prs.slides.add_slide(blank_layout)
    set_slide_background(s9)
    add_header(s9, "Tech Stack", "Why Hybrid Architecture: Python Core + Next.js UI",
               "Combining Python's deep learning accuracy with Next.js/React's lightning-fast user experience.")

    add_card(s9, Inches(0.8), Inches(2.0), Inches(5.6), Inches(4.8), "Python (Backend & Vision Engine)", [
        "Core Libraries: OpenCV, PyTorch, Torchvision, FastAPI, SQLite.",
        "",
        "Why Python for Vision?",
        "• Unbeatable 99.8% LFW accuracy with deep ArcFace embeddings.",
        "• Sub-pixel 6-point / 68-point facial landmark regression.",
        "• Fast matrix dot product cosine similarity (sub-15ms for 50,000 faces).",
        "• Robust multithreading and GPU-acceleration support.",
        "• Powers the Universal Watch Folder CLI server.",
        "",
        "Conclusion: In-browser JavaScript face models struggle with extreme angles and low light; Python ensures production-grade accuracy."
    ], PRIMARY)

    add_card(s9, Inches(6.8), Inches(2.0), Inches(5.6), Inches(4.8), "Next.js + React (Frontend)", [
        "Core Stack: Next.js 14 (App Router), React 18, TypeScript, Tailwind CSS.",
        "",
        "Why Next.js & React for UI?",
        "• WebRTC camera stream via navigator.mediaDevices.getUserMedia.",
        "• Zero app install friction: Works instantly on any mobile or desktop browser.",
        "• Client-side image canvas preview and capture guidelines.",
        "• Dynamic multi-event accordion grouping and batch download management.",
        "• Developer face bounding box & quality score inspection overlay.",
        "",
        "Conclusion: Clean, responsive, modern interface with zero user latency."
    ], INDIGO)

    # =========================================================
    # SLIDE 10: Current Project Status & Roadmap
    # =========================================================
    s10 = prs.slides.add_slide(blank_layout)
    set_slide_background(s10)
    add_header(s10, "Progress & Roadmap", "Current Development Status & Next Steps",
               "Frontend and core vision pipeline are operational; ready for dataset calibration.")

    add_card(s10, Inches(0.8), Inches(2.0), Inches(5.6), Inches(4.8), "Completed Components", [
        "✓ Full Next.js 14 Frontend directly in project root:",
        "  • Universal Multi-Event Search & Grouped Gallery.",
        "  • Single-Click Event Batch Download & Lightbox Viewer.",
        "  • WebRTC Camera Selfie Capture & Consent Notice Modal.",
        "  • Organizer Watch Folder Console & Ingestion Dashboard.",
        "  • Interactive Face Bounding Box & Quality Inspector.",
        "  • 18-Step A-to-Z Workflow Infographic Viewer.",
        "",
        "✓ Computer Vision Engine & Recognition Pipeline:",
        "  • Multi-face detector, Laplacian blur quality gate, 512-D ArcFace model.",
        "",
        "✓ Universal Watch Folder CLI Daemon:",
        "  • Auto-indexing universal_folder/ and clustering into face_clusters.json.",
        "",
        "✓ Automated Test Suite (pytest): 100% Passing (5/5 tests)."
    ], EMERALD)

    add_card(s10, Inches(6.8), Inches(2.0), Inches(5.6), Inches(4.8), "Upcoming Phases (Next Steps)", [
        "Phase 2: Primary Dataset Acquisition:",
        "• Collect permissioned volunteer dataset (weddings and college events).",
        "• Diverse indoor/outdoor illumination, crowds, and angle variations.",
        "",
        "Phase 3: Calibration & Empirical Benchmarking:",
        "• Calibrate similarity threshold to optimize Precision & Recall curves.",
        "• Evaluate false positive rates on group photos.",
        "",
        "Phase 4: Production Hardening & Cloud Deployment:",
        "• Deploy on VPS with HTTPS for trusted mobile camera permissions.",
        "• Mobile app wrapper (PWA / React Native) for Android & iOS.",
        "• Multi-modal re-identification research (hair style, clothing cues)."
    ], PRIMARY_DARK)

    # =========================================================
    # SLIDE 11: Conclusion & Q&A (Presenter: Mohammad Arsh)
    # =========================================================
    s11 = prs.slides.add_slide(blank_layout)
    set_slide_background(s11)

    card11 = s11.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.5), Inches(1.0), Inches(10.333), Inches(5.5))
    card11.fill.solid()
    card11.fill.fore_color.rgb = WHITE
    card11.line.color.rgb = CARD_BORDER
    card11.line.width = Pt(1.5)

    tf11 = card11.text_frame
    tf11.word_wrap = True
    tf11.vertical_anchor = MSO_ANCHOR.MIDDLE
    tf11.margin_left = Inches(0.8)
    tf11.margin_right = Inches(0.8)

    p = tf11.paragraphs[0]
    p.text = "FindZora"
    p.font.name = "Arial"
    p.font.size = Pt(40)
    p.font.bold = True
    p.font.color.rgb = PRIMARY
    p.space_after = Pt(6)

    p2 = tf11.add_paragraph()
    p2.text = "Thank You! Questions & Discussion"
    p2.font.name = "Arial"
    p2.font.size = Pt(24)
    p2.font.bold = True
    p2.font.color.rgb = TEXT_DARK
    p2.space_after = Pt(20)

    p3 = tf11.add_paragraph()
    p3.text = "Key Takeaways:"
    p3.font.name = "Arial"
    p3.font.size = Pt(14)
    p3.font.bold = True
    p3.font.color.rgb = INDIGO
    p3.space_after = Pt(8)

    bullets = [
        "• Precomputed 512-D ArcFace vectors eliminate repetitive face processing on guest queries.",
        "• Universal Watch Folder CLI turns local/VPS folders into automated self-indexing servers.",
        "• Universal Multi-Event Search groups photos by event with 1-click batch downloads.",
        "• Privacy-by-Design: Ephemeral selfie processing, event isolation, and wrong-match reporting."
    ]
    for b in bullets:
        p_b = tf11.add_paragraph()
        p_b.text = b
        p_b.font.name = "Arial"
        p_b.font.size = Pt(12)
        p_b.font.color.rgb = TEXT_BODY
        p_b.space_after = Pt(4)

    p_b.space_after = Pt(24)

    p_pres = tf11.add_paragraph()
    p_pres.text = "Presenter: Mohammad Arsh"
    p_pres.font.name = "Arial"
    p_pres.font.size = Pt(16)
    p_pres.font.bold = True
    p_pres.font.color.rgb = PRIMARY_DARK

    p_mca = tf11.add_paragraph()
    p_mca.text = "Master of Computer Applications (MCA) Final Project"
    p_mca.font.name = "Arial"
    p_mca.font.size = Pt(12)
    p_mca.font.color.rgb = TEXT_MUTED

    # Save presentation
    output_path = Path("FindZora_Project_Presentation.pptx")
    prs.save(str(output_path))
    print(f"Presentation saved successfully to: {output_path.resolve()}")

if __name__ == "__main__":
    create_presentation()
