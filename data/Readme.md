🚀 VisionPack AI
Smart Object Detection • Quality Check • Feedback Loop • Auto-Retraining • Dashboard

VisionPack AI is an end-to-end computer-vision system built for packaging automation.
It can detect objects in real time, analyze image quality, collect human feedback through WhatsApp, retrain itself, and show everything on a clean monitoring dashboard.

This project shows my ability to build a complete production-style AI system — including backend, automation, ML model handling, dashboards, caching, testing, and CI/CD.

🔥 What VisionPack AI Can Do
✔ Real-time Object Detection (YOLOv8)

FastAPI endpoint to upload an image

Returns bounding boxes, class name & confidence

Works fast and supports GPU/CPU

✔ Frame Quality Analysis

Every prediction also calculates:

Blur score

Brightness

Noise level

Frame rate (for video)

Motion detection

These help ensure packaging cameras are working correctly.

✔ WhatsApp Feedback Integration

Using Twilio:

After detection, a worker can confirm the result by replying “yes” or “no”

Incorrect results are stored for model improvements

All feedback is logged inside data/feedback/log.json

✔ Smart Caching (Super Fast Predictions)

If the same image is uploaded again:

The system returns cached output instantly

Great for reducing inference time

Cuts compute by 60–80%

✔ Auto-Retraining Pipeline

When enough feedback is collected:

System checks if retraining is needed

Launches a small training job

Automatically loads the new YOLO model into the API

Logs an event MODEL_UPDATED

Recruiters love this part — it shows automation + ML engineering skills.

✔ Beautiful Streamlit Monitoring Dashboard

The dashboard shows:

Live object detection results

Full quality metrics

Prediction speed

System health & performance logs
Runs with:

streamlit run src/dashboard/app.py


Opens at → http://localhost:8501

✔ Performance Monitoring

Every prediction is logged in monitor/metrics.json:

Inference time

Detection count

Average confidence

Cache hit / miss

Image size

Great for debugging and optimization.

✔ Complete Testing Suite (Pytest)

Tests include:

API functionality

Caching

Quality metrics

Dashboard smoke test

Performance logger

Video utilities

Run all tests:

pytest -q

✔ GitHub CI/CD

A full GitHub Actions workflow:

Installs dependencies

Runs all tests

Blocks merge if anything fails

Helps keep the project clean and production-ready.

✔ Benchmark Script (FPS + Latency)

Test YOLO performance:

python -m scripts.benchmark --image bus.jpg --iterations 30


Shows:

Avg latency

FPS

Preprocess / inference / postprocess speed

🏗 Project Structure
visionpack-ai/
 ├── src/
 │   ├── api/            → FastAPI backend
 │   ├── automation/     → retraining + event engine
 │   ├── quality/        → blur / brightness / noise metrics
 │   ├── feedback/       → WhatsApp bot
 │   ├── dashboard/      → Streamlit UI
 │   ├── monitor/        → performance metrics
 │   ├── utils/          → cache + video helper functions
 │   └── models/         → YOLO weights
 ├── tests/              → Pytest suite
 ├── scripts/benchmark.py
 ├── .github/workflows/ci.yml
 ├── requirements.txt
 └── README.md

🚀 How To Run Everything
1️⃣ Activate virtual environment
.\venv\Scripts\activate

2️⃣ Run the FastAPI backend
uvicorn src.api.main:app --reload --port 8000

3️⃣ Start the dashboard
streamlit run src/dashboard/app.py


Dashboard → http://localhost:8501

📡 Test the API
curl -X POST "http://localhost:8000/predict" -F "file=@bottles.jpg"


Example Output:

{
  "detections": [
    {
      "bbox": [148,128,411,921],
      "class": "bottle",
      "conf": 0.95
    }
  ],
  "quality": {
    "blur_score": 551.24,
    "brightness": 0.59,
    "noise_level": 7.09,
    "frame_rate": null,
    "motion_detected": null
  },
  "runtime_ms": 498.53,
  "cached": false
}