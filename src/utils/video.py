# src/utils/video.py

from __future__ import annotations
from typing import Dict, List, Tuple
import cv2
import numpy as np
from ultralytics import YOLO

from src.quality.quality_check import analyze_frame


def process_video(
    model: YOLO,
    video_bytes: bytes,
    conf: float = 0.4,
    frame_skip: int = 3,
) -> Dict:
    # write temp file
    import tempfile, os

    with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as tmp:
        tmp.write(video_bytes)
        tmp_path = tmp.name

    cap = cv2.VideoCapture(tmp_path)
    fps = cap.get(cv2.CAP_PROP_FPS) or 0.0

    all_detections: List[Dict] = []
    frame_count = 0

    while True:
        ret, frame_bgr = cap.read()
        if not ret:
            break
        frame_count += 1
        if frame_count % frame_skip != 0:
            continue

        frame_rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
        results = model.predict(frame_rgb, conf=conf, verbose=False)

        dets = []
        for box in results[0].boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            dets.append(
                {
                    "bbox": [x1, y1, x2, y2],
                    "class": model.names[int(box.cls[0])],
                    "conf": float(box.conf[0]),
                }
            )

        quality = analyze_frame(frame_rgb, fps=fps)
        all_detections.append(
            {"frame_index": frame_count, "detections": dets, "quality": quality}
        )

    cap.release()
    os.remove(tmp_path)

    total_objects = sum(len(f["detections"]) for f in all_detections)

    return {
        "frames_processed": len(all_detections),
        "total_objects": total_objects,
        "fps": fps,
        "frames": all_detections,
    }
