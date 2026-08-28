<div align="center">

<!-- Tech Stack Badges -->
<p>
  <img src="https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/PyTorch-2.0+-EE4C2C?style=for-the-badge&logo=pytorch&logoColor=white" />
  <img src="https://img.shields.io/badge/YOLOv8-Ultralytics-111F68?style=for-the-badge" />
  <img src="https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white" />
  <img src="https://img.shields.io/badge/OpenCV-5C3EE8?style=for-the-badge&logo=opencv&logoColor=white" />
  <img src="https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white" />
  <img src="https://img.shields.io/badge/PyTest-0A9EDC?style=for-the-badge&logo=pytest&logoColor=white" />
</p>

# VisionPack AI

**End-to-End Aerial Object Detection with Human-in-the-Loop Feedback & Auto-Retraining**

[Overview](#-overview) •
[Features](#-key-features) •
[Architecture](#-system-architecture) •
[Structure](#-project-structure) •
[Quick Start](#-quick-start) •
[API](#-api-reference) •
[HITL](#-human-in-the-loop-hitl-pipeline) •
[Results](#-performance-benchmarks)

</div>

---

## 📌 Overview

Production-grade computer vision system that performs real-time object detection on aerial drone imagery using **YOLOv8** fine-tuned on the **VisDrone dataset** (~6,200 images). Features a complete MLOps pipeline including a FastAPI inference backend, CVAT-powered annotation feedback, Twilio WhatsApp human-in-the-loop correction, and automated model retraining for continuous improvement.

| Metric          | Value                          |
|-----------------|---------------------------------|
| Dataset         | VisDrone 2019 (Aerial Imagery)  |
| Model           | YOLOv8n → YOLOv8m (upgradable)  |
| Images          | ~6,200 annotated aerial frames  |
| Classes         | 10 (pedestrian, vehicle, bicycle, etc.) |
| Inference       | ~120 ms on CPU                  |
| API Framework   | FastAPI + Uvicorn               |
| Feedback Loop   | WhatsApp (Twilio) + CVAT        |
| Dashboard       | Streamlit (Port 8501)           |

---

## 🔥 Key Features

| # | Feature                     | Description                                                                                   |
|---|------------------------------|-------------------------------------------------------------------------------------------------|
| 1 | ⚡ Real-Time Detection        | YOLOv8 inference on aerial imagery with bounding boxes, class labels, and confidence scores    |
| 2 | 🎯 VisDrone Optimized         | Fine-tuned for small, dense objects typical in drone-view datasets (pedestrians, vehicles, bicycles) |
| 3 | 💬 Human-in-the-Loop          | CVAT annotation review + Twilio WhatsApp API for instant worker feedback and correction        |
| 4 | 🔄 Auto-Retraining            | Triggered retraining pipeline when feedback volume crosses threshold; hot-swaps model without downtime |
| 5 | 📊 Performance Monitoring     | Live latency tracking, detection counts, and model health metrics via Streamlit                |
| 6 | 🧪 Production Testing         | Full PyTest coverage for API, inference, cache, quality, and feedback logic                    |
| 7 | 🚀 CI/CD Ready                | GitHub Actions workflow for automated testing on every push                                    |

---

## 🏗 System Architecture

```
┌─────────────────┐      HTTP/REST       ┌──────────────────┐
│   Streamlit     │ ◄──────────────────► │   FastAPI        │
│   Dashboard     │     (Port 8501)      │   Backend        │
│ (src/dashboard) │                      │  (src/api)       │
│                 │                      │   Port 8000      │
└─────────────────┘                      └────────┬─────────┘
        │                                          │
        │ reads logs                               │ uploads
        ▼                                          ▼
┌──────────────────────────────────────────────────────────────┐
│                     Core Processing Layer                    │
│  ┌──────────────┐   ┌──────────────┐   ┌──────────────┐      │
│  │   YOLOv8     │   │   Quality    │   │  Prediction  │      │
│  │  Inference   │   │   Analyzer   │   │    Cache     │      │
│  │  (VisDrone)  │   │              │   │  (SHA-256)   │      │
│  └──────────────┘   └──────────────┘   └──────────────┘      │
│         │                   │                   │            │
│         └───────────────────┼───────────────────┘            │
│                              ▼                               │
│               ┌─────────────────────────┐                    │
│               │   Performance Logger    │                    │
│               │   (src/monitor) JSONL   │                    │
│               └─────────────────────────┘                    │
└──────────────────────────────────────────────────────────────┘
        │                                          │
        ▼                                          ▼
┌─────────────────┐                      ┌──────────────────┐
│  Event Engine   │  ──QUALITY_ISSUE──►  │  Auto-Retrainer  │
│  & Listeners    │  ──MODEL_UPDATED──►  │  (src/automation)│
│ (src/automation)│                      └──────────────────┘
└─────────────────┘                                  │
        │                                            │
        ▼                                            ▼
┌─────────────────┐                        ┌──────────────────┐
│  WhatsApp Bot   │                        │  Feedback Store  │
│  (Twilio API)   │                        │ (data/feedback)  │
│  + CVAT         │                        │  log.json        │
└─────────────────┘                        └──────────────────┘
```

---

## 🛠 Tech Stack

| Layer          | Technology                     | Purpose                                            |
|-----------------|---------------------------------|------------------------------------------------------|
| Backend         | FastAPI + Uvicorn               | Async REST API with auto-generated Swagger docs      |
| ML Model        | Ultralytics YOLOv8              | State-of-the-art object detection on VisDrone         |
| CV Processing   | OpenCV + Pillow + NumPy         | Image preprocessing, augmentation, array ops          |
| Dataset         | VisDrone 2019 (~6,200 images)   | Aerial imagery with 10 object categories               |
| Feedback        | CVAT + Twilio WhatsApp API      | Human annotation review and instant messaging          |
| Training        | PyTorch + Ultralytics           | Model fine-tuning and retraining orchestration          |
| Dashboard       | Streamlit                       | Real-time monitoring UI                                 |
| Caching         | In-Memory Dict + SHA-256        | Zero-dependency, sub-millisecond lookups                |
| Events          | Custom Event Engine             | Decoupled automation without heavy brokers               |
| Monitoring      | psutil + JSONL logs             | Lightweight, no external DB needed                        |
| Testing         | PyTest + FastAPI TestClient     | Unit & integration test coverage                            |
| CI/CD           | GitHub Actions                  | Automated quality gates                                       |

---

## 📁 Project Structure

```
visionpack-ai/
├── .github/
│   └── workflows/
│       └── ci.yml               # GitHub Actions pipeline
├── app/                         # Application layer
├── data/
│   ├── datasets/
│   │   └── visdrone/            # VisDrone dataset (~6,200 images)
│   │       ├── convert_visdrone.py
│   │       ├── images/
│   │       │   ├── train/
│   │       │   └── val/
│   │       ├── labels/
│   │       │   ├── train/
│   │       │   └── val/
│   │       ├── train.cache
│   │       ├── val.cache
│   │       └── dataset.yaml     # YOLO data config
│   └── feedback/
│       ├── log.json             # Human feedback store
│       ├── whatsapp_bot.py      # Twilio webhook handler
│       ├── best.pt              # Best model checkpoint
│       └── retrain.py           # Retraining trigger
├── runs/
│   └── detect/                  # Training runs (train-1 to train-9, visdrone-100epochs, visdrone-real)
│       ├── predict/             # Inference outputs
│       ├── train/               # Training artifacts
│       └── ...
├── scripts/
│   └── benchmark.py             # FPS & latency profiler
├── src/
│   ├── api/
│   │   └── main.py              # FastAPI app, /predict, /status, /retrain
│   ├── automation/
│   │   ├── controller.py        # Post-detection decision logic
│   │   ├── event_engine.py      # Event bus (QUALITY_ISSUE, MODEL_UPDATED)
│   │   ├── listeners.py         # Event subscribers
│   │   └── retrainer.py         # Auto-retraining orchestrator
│   ├── dashboard/
│   │   └── app.py               # Streamlit monitoring UI (Port 8501)
│   ├── feedback/
│   │   ├── __init__.py
│   │   └── retrain.py           # Feedback-based retraining logic
│   ├── models/                  # YOLO .pt weights
│   ├── monitor/
│   │   └── performance.py       # Inference logging to JSONL
│   ├── quality/
│   │   └── quality_check.py     # Blur, brightness, noise, motion analysis
│   └── utils/
│       ├── cache.py             # SHA-256 keyed LRU cache
│       ├── video.py             # Video frame extraction & batching
│       └── __init__.py
├── tests/                       # PyTest suite
│   ├── test_cache.py
│   ├── test_dashboard.py
│   ├── test_performance_logger.py
│   ├── test_predict.py
│   ├── test_quality.py
│   ├── test_status.py
│   └── test_video.py
├── .env                         # Environment variables
├── .gitignore
├── bus.jpg                      # Sample test image
├── fix_labels.py                # Label format converter
├── pytest.ini                   # PyTest configuration
├── requirements.txt             # Python dependencies
├── visdrone_data.tar            # Dataset archive
└── yolov8n.pt                   # Pre-trained YOLOv8n weights
```

---

## 🚀 Quick Start

### Prerequisites

- Python 3.10+
- (Optional) CUDA for GPU acceleration

### 1. Clone & Setup

```bash
git clone https://github.com/DeepeshSherawat04/visionpack.git
cd visionpack-ai
python -m venv venv

# Windows
.\venv\Scripts\activate

# macOS / Linux
source venv/bin/activate

pip install -r requirements.txt
```

### 2. Prepare VisDrone Dataset

```bash
# Extract and convert VisDrone annotations to YOLO format
python data/datasets/visdrone/convert_visdrone.py
```

### 3. Train on VisDrone

```bash
# Using Ultralytics CLI (configured in dataset.yaml)
# Model: yolov8n.pt | Epochs: 30 | Image Size: 640 | Batch: 16
yolo detect train model=yolov8n.pt data=data/datasets/visdrone/dataset.yaml epochs=30 imgsz=640 batch=16

# Or use existing trained runs in runs/detect/visdrone-100epochs/
```

### 4. Start the Backend

```bash
uvicorn src.api.main:app --reload --port 8000
```

📡 API Docs: `http://localhost:8000/docs`

### 5. Start the Dashboard (New Terminal)

```bash
streamlit run src/dashboard/app.py
```

📊 Dashboard: `http://localhost:8501`

### 6. Run Tests

```bash
pytest -q
```

---

## 📡 API Reference

### `POST /predict`

Upload an aerial image for object detection + quality analysis.

**Request:** `multipart/form-data` with `file` field

**Response:**

```json
{
  "detections": [
    {
      "bbox": [1250, 480, 1320, 560],
      "class": "pedestrian",
      "conf": 0.91
    },
    {
      "bbox": [890, 520, 1100, 610],
      "class": "car",
      "conf": 0.88
    }
  ],
  "quality": {
    "blur_score": 551.24,
    "brightness": 0.59,
    "noise_level": 7.09,
    "frame_rate": null,
    "motion_detected": null
  },
  "runtime_ms": 118.4,
  "cached": false,
  "model_version": "visdrone_yolov8n_v1.2"
}
```

### `GET /status`

System health check with memory, CPU usage, and model version.

### `POST /retrain`

Trigger model retraining if enough feedback is collected.

---

## 💬 Human-in-the-Loop (HITL) Pipeline

| Step | Action                                                   | Tool                       |
|------|-----------------------------------------------------------|------------------------------|
| 1    | Model predicts on new aerial image                        | YOLOv8 + FastAPI              |
| 2    | Low-confidence / uncertain detection flagged               | Custom logic + Quality Analyzer |
| 3    | Image sent to worker via WhatsApp                          | Twilio API                     |
| 4    | Worker reviews and replies: `yes` or `no: [correct_label]`  | WhatsApp                        |
| 5    | Corrections exported to CVAT for annotation refinement     | CVAT                              |
| 6    | Feedback stored in `data/feedback/log.json`                 | JSON Store                          |
| 7    | Feedback count > threshold triggers retraining              | Event Engine                          |
| 8    | New model evaluated and hot-swapped automatically           | Retrainer                              |

---

## 🔄 Auto-Retraining & Performance Monitoring

```
Feedback Count > Threshold (e.g., 50 corrections)?
              │
              ▼
    ┌─────────────────┐
    │  Export CVAT    │
    │  Annotations    │
    └────────┬────────┘
              │
              ▼
    ┌─────────────────┐
    │  Retrain YOLOv8 │ ──► VisDrone dataset + new feedback
    │  on Mixed Data  │ ──► Validation mAP check
    └────────┬────────┘
              │
              ▼
    ┌─────────────────┐
    │  Model Passes   │ ──► Replace old weights (hot-swap)
    │  Validation?    │ ──► Emit MODEL_UPDATED event
    └─────────────────┘
```

**Monitored Metrics**

- Inference latency (ms)
- Detection count per class
- Worker feedback accuracy
- Model mAP@0.5 over time
- Frame quality (blur, brightness, noise)

---

## 📊 Performance Benchmarks

*Run on Intel i5 / 8GB RAM / CPU-only / VisDrone 640×640*

| Metric                          | Value                    |
|-----------------------------------|-----------------------------|
| Average Inference Latency          | ~118 ms                       |
| Cache Hit Latency                  | < 1 ms                          |
| First Load (Model + Warmup)         | ~3.8 s                            |
| VisDrone Classes Supported          | 10                                  |
| Input Image Formats                 | JPG, JPEG, PNG                        |
| Concurrent Requests                 | Async via FastAPI                       |

```bash
python -m scripts.benchmark --image bus.jpg --iterations 30
```

---

## 🎯 VisDrone Dataset Classes

| ID | Class      | ID | Class            |
|----|-------------|----|--------------------|
| 0  | pedestrian  | 5  | bus                  |
| 1  | person      | 6  | truck                  |
| 2  | bicycle     | 7  | motor                    |
| 3  | car         | 8  | tricycle                   |
| 4  | van         | 9  | awning-tricycle               |

---

## 🧪 Production-Grade Testing

```bash
pytest -q
```

| Test                         | Status |
|--------------------------------|----------|
| API prediction endpoint         | ✅         |
| Cache hit/miss logic            | ✅         |
| Quality metric calculations     | ✅         |
| Performance logger              | ✅         |
| Dashboard smoke test            | ✅         |
| Video processing utilities      | ✅         |

---

## 🗺 Roadmap

- [x] Integrate VisDrone dataset (~6,200 images)
- [x] YOLOv8 training pipeline (30 epochs, 640×640)
- [x] FastAPI inference backend
- [x] Streamlit monitoring dashboard
- [x] Human-in-the-Loop WhatsApp feedback
- [x] Automated retraining trigger
- [ ] Integrate YCloud WhatsApp API (free tier)
- [ ] Add GPU support toggle
- [ ] Export metrics to Prometheus/Grafana
- [ ] Deploy with Docker + AWS/GCP
- [ ] Add multi-model A/B testing

---

## 🎯 What Makes This Project Different?

Most repos showing "YOLO + FastAPI" stop at: *"Upload image → get bounding box."*

**VisDrone Detection** goes further:

- **Self-Improving** — It doesn't just detect; it learns from human feedback via WhatsApp and retrains itself.
- **Quality-Aware** — It validates camera health (blur, brightness, noise) before trusting detections.
- **Production-Ready** — Caching, logging, health checks, automated tests, and CI/CD, not just a notebook.
- **Observable** — Dashboard shows historical trends, not just one-off predictions.
- **Aerial-Optimized** — Specifically trained on VisDrone for small, dense object detection from drone perspectives.

---

## 👤 Author

**Deepesh Sherawat**

🔗 [LinkedIn](https://www.linkedin.com/in/deepesh-sherawat-1a595523b) • 💻 [GitHub](https://github.com/DeepeshSherawat04) • 📧 [Email](mailto:deepeshsherawat1290@gmail.com)

Built to demonstrate production-grade AI system design — from aerial dataset curation to deployed inference with continuous human feedback loops.

<div align="center">

⭐ **Star this repo if you found it useful!**

</div>