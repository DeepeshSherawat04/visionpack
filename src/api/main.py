# src/api/main.py

from fastapi import FastAPI, UploadFile, File
from ultralytics import YOLO
from PIL import Image
import numpy as np
import io
import time

# Import automation logic
from src.automation.controller import handle_automation
from src.data.feedback.whatsapp_bot import router as feedback_router

# New imports for advanced features
from src.quality.quality_check import analyze_frame
from src.utils.cache import prediction_cache
from src.monitor.performance import log_inference
from src.automation.event_engine import emit_event, EventType
from src.automation.listeners import register_all_listeners
from src.utils.video import process_video
from src.automation.retrainer import should_retrain, run_retrain

# psutil is optional – if not installed, status() will still work
try:
    import psutil
except ImportError:
    psutil = None

app = FastAPI(title="VisionPack AI API")

APP_START_TIME = time.time()

# Load YOLO model
model = YOLO("yolov8n.pt")

# Register any event listeners (quality issue, model updated, etc.)
register_all_listeners()


@app.get("/")
def root():
    return {"message": "VisionPack AI API running. Use /predict to upload images."}


@app.get("/status")
def status():
    """Simple health/status endpoint."""
    uptime_sec = time.time() - APP_START_TIME
    info = {
        "status": "ok",
        "model_loaded": True,
        "uptime_seconds": uptime_sec,
    }

    if psutil is not None:
        process = psutil.Process()
        mem = process.memory_info()
        info["memory_mb"] = mem.rss / (1024 * 1024)
        info["cpu_percent"] = psutil.cpu_percent(interval=0.1)

    return info


@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    """
    Image prediction endpoint with:
    - caching
    - quality metrics
    - performance logging
    - quality issue events
    - automation hook
    """
    # Read file bytes
    raw_bytes = await file.read()

    # ---- CACHING ---------------------------------------------------------
    cache_key = prediction_cache.make_key(raw_bytes)
    cached = prediction_cache.get(cache_key)
    if cached is not None:
        # If you still want automation even on cached responses:
        handle_automation(cached["detections"])
        return {**cached, "cached": True}

    # ---- IMAGE LOAD ------------------------------------------------------
    image = Image.open(io.BytesIO(raw_bytes)).convert("RGB")
    np_image = np.array(image)

    # ---- YOLO INFERENCE + TIMING ----------------------------------------
    start_time = time.time()
    results = model.predict(np_image, conf=0.4)
    inference_time_ms = (time.time() - start_time) * 1000.0

    # ---- BUILD DETECTIONS LIST ------------------------------------------
    detections = []
    for box in results[0].boxes:
        x1, y1, x2, y2 = map(int, box.xyxy[0])
        detections.append(
            {
                "bbox": [x1, y1, x2, y2],
                "class": model.names[int(box.cls[0])],
                "conf": float(box.conf[0]),
            }
        )

    avg_conf = (
        sum(d["conf"] for d in detections) / len(detections)
        if detections
        else 0.0
    )

    # ---- QUALITY METRICS -------------------------------------------------
    quality = analyze_frame(np_image)

    # ---- PERFORMANCE LOGGING --------------------------------------------
    log_inference(
        source="api",
        inference_time_ms=inference_time_ms,
        num_detections=len(detections),
        avg_conf=avg_conf,
        image_shape=list(np_image.shape),
    )

    # ---- QUALITY ISSUE EVENT --------------------------------------------
    # Adjust thresholds as you like
    if (
        quality.get("blur_score") is not None
        and quality["blur_score"] < 50
    ) or (
        quality.get("brightness") is not None
        and quality["brightness"] < 0.2
    ):
        emit_event(
            EventType.QUALITY_ISSUE,
            source="api",
            runtime_ms=inference_time_ms,
            num_detections=len(detections),
            avg_conf=avg_conf,
            image_shape=list(np_image.shape),
            quality=quality,
        )

    # ---- AUTOMATION HOOK (existing behavior) ----------------------------
    handle_automation(detections)

    # ---- RESPONSE + CACHE STORE -----------------------------------------
    response = {
        "detections": detections,
        "quality": quality,
        "runtime_ms": inference_time_ms,
        "cached": False,
    }

    prediction_cache.set(cache_key, response)

    return response


@app.post("/predict-video")
async def predict_video(file: UploadFile = File(...)):
    """
    Video prediction endpoint: summarize detections + quality per frame.
    """
    raw_bytes = await file.read()
    summary = process_video(model, raw_bytes, conf=0.4)

    log_inference(
        source="api-video",
        inference_time_ms=0.0,
        num_detections=summary["total_objects"],
        avg_conf=0.0,
        image_shape=[],
    )

    return summary


@app.post("/retrain")
def retrain_model():
    """
    Trigger a retrain using feedback samples once there is enough data.
    """
    if not should_retrain():
        return {"status": "skipped", "reason": "not_enough_feedback"}

    global model
    new_path = run_retrain()
    model = YOLO(new_path)

    emit_event(EventType.MODEL_UPDATED, new_model_path=new_path)

    return {"status": "ok", "new_model": new_path}


# ✅ Register WhatsApp feedback router
app.include_router(feedback_router)
