from fastapi import FastAPI, UploadFile, File
from ultralytics import YOLO
from PIL import Image
import numpy as np
import io

# Import automation logic
from src.automation.controller import handle_automation
from src.feedback.whatsapp_bot import router as feedback_router

app = FastAPI(title="VisionPack AI API")

# Load YOLO model
model = YOLO("yolov8n.pt")

@app.get("/")
def root():
    return {"message": "VisionPack AI API running. Use /predict to upload images."}

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    image = Image.open(io.BytesIO(await file.read())).convert("RGB")
    results = model.predict(np.array(image), conf=0.4)

    detections = []
    for box in results[0].boxes:
        x1, y1, x2, y2 = map(int, box.xyxy[0])
        detections.append({
            "bbox": [x1, y1, x2, y2],
            "class": model.names[int(box.cls[0])],
            "conf": float(box.conf[0])
        })

    # 🔁 Simulate automation behavior
    handle_automation(detections)

    return {"detections": detections}


# ✅ Register WhatsApp feedback router
app.include_router(feedback_router)
