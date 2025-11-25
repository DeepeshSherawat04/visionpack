Smart Object Detection • Quality Monitoring • Feedback Loop • Auto-Retraining • Streamlit Dashboard
VisionPack AI is an end-to-end computer vision system built for packaging automation.
It detects objects in real time using YOLOv8, checks the quality of incoming frames, collects human feedback through WhatsApp, automatically retrains the model when needed, and displays everything on a clean, modern Streamlit dashboard.

This project reflects my ability to build complete production-style AI systems, including:

FastAPI backend

Real-time object detection

Computer Vision pipelines

Automation & retraining flows

Caching & performance optimization

Streamlit dashboards

CI/CD pipeline

Automated testing (PyTest)

🌟 Features
🔥 Real-Time Object Detection

Built with YOLOv8

FastAPI endpoint: /predict

Returns bounding boxes, class labels, and confidence

Lightweight & production-ready

📷 Frame Quality Analysis

Each prediction also returns:

Blur score

Brightness level

Noise level

Motion detection

Frame rate (if video)

This ensures that the camera and environment are suitable for real-world industrial use.

💬 WhatsApp Feedback Loop (Human-in-the-Loop AI)

Using Twilio WhatsApp API:

Worker receives detected image

Replies “yes” if prediction was correct

Replies “no” + corrected label

Feedback is saved in:

data/feedback/log.json


This makes the model improve over time.

⚡ Smart Caching System

Detects duplicate incoming images

Saves prediction + quality output in cache

Instant response on repeat requests

Reduces inference time significantly

🤖 Auto-Retraining Pipeline

The system automatically:

Reads feedback

Checks if retraining is needed

Launches a mini retraining job

Replaces the YOLO model with the newly trained model

Emits a system event: MODEL_UPDATED

This simulates real industrial AI lifecycle automation.

📊 Streamlit Monitoring Dashboard

A dedicated UI for monitoring detections & performance:

Upload image → run YOLO

View real-time results

Quality metrics panel

Performance stats (latency, cache hits, etc.)

Start dashboard:

streamlit run src/dashboard/app.py


Dashboard opens at:
👉 http://localhost:8501

📈 Performance & System Monitoring

Every prediction is logged into:

monitor/metrics.json


Includes:

Inference time

Detection count

Average confidence

Image dimensions

Cache hit/miss

Runtime metadata

🧪 Full Testing Suite (PyTest)

Includes tests for:

API prediction

Caching

Quality metrics

Performance logging

Dashboard smoke tests

Video utilities

Status endpoints

Run all tests:

pytest -q

⚙️ GitHub CI/CD (GitHub Actions)

The project includes a pipeline that:

Installs dependencies

Runs all tests

Fails automatically if anything breaks

File:

.github/workflows/ci.yml

🧪 Benchmark Script (FPS + Latency Test)

Run:

python -m scripts.benchmark --image bus.jpg --iterations 30


Shows:

Preprocess time

Inference time

Postprocess time

Average latency

FPS

Great for debugging YOLO performance.

🏗 Project Structure
visionpack-ai/
 ├── src/
 │   ├── api/            # FastAPI backend
 │   ├── automation/     # retraining + event engine
 │   ├── quality/        # blur/brightness/noise metrics
 │   ├── feedback/       # WhatsApp feedback bot
 │   ├── dashboard/      # Streamlit dashboard
 │   ├── monitor/        # performance logs
 │   ├── utils/          # cache + video helpers
 │   └── models/         # YOLO weights
 ├── tests/              # Pytest suite
 ├── scripts/            # benchmark script
 ├── .github/workflows/ci.yml
 ├── requirements.txt
 └── README.md

🚀 How to Run
1. Clone the Repo
git clone https://github.com/DeepeshSherawat04/visionpack.git
cd visionpack

2. Activate Virtual Environment
.\venv\Scripts\activate

3. Start Backend (FastAPI)
uvicorn src.api.main:app --reload --port 8000

4. Start Dashboard (Streamlit)
streamlit run src/dashboard/app.py

📡 Example API Response
{
  "detections": [
    {
      "bbox": [148, 128, 411, 921],
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
