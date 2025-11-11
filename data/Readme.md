🧠 What is VisionPack AI?

VisionPack AI is an intelligent computer vision project that can detect, classify, and automate the handling of packaging items like boxes and bottles using AI.
It also collects feedback through WhatsApp (Twilio API) to keep improving its accuracy over time — just like a learning system that gets smarter with every correction.

It’s built with YOLOv8, FastAPI, and Streamlit for a full end-to-end experience — from detection to feedback to retraining and dashboard visualization.

🚀 Main Features

🧩 Detects and classifies objects using YOLOv8

⚙️ Runs on a FastAPI backend for easy image uploads and predictions

🔁 Simulates automation like sorting on left/right conveyors

💬 Uses WhatsApp feedback (Twilio) for correction and learning

📈 Retrains automatically to improve accuracy

🖥️ Has a Streamlit dashboard to upload and visualize detections

🛠️ Tech Stack

Python 3.11+

YOLOv8 (Ultralytics)

FastAPI – Backend API

OpenCV, NumPy, PIL – Image processing

Twilio API – WhatsApp integration

Streamlit – Interactive dashboard

PyTorch – Model training

📁 Project Structure
visionpack-ai/
│
├── src/
│   ├── api/              # FastAPI backend routes
│   ├── automation/       # Conveyor simulation logic
│   ├── feedback/         # WhatsApp feedback + retraining
│   ├── dashboard/        # Streamlit dashboard UI
│   └── models/, utils/   # Helper scripts
│
├── data/                 # Datasets and feedback logs
├── experiments/          # Trained YOLO models
├── runs/                 # Prediction outputs
├── yolov8n.pt            # Base model
└── .env                  # Twilio credentials

⚙️ How to Set Up and Run
Step 1: Clone the project
git clone https://github.com/<your-username>/visionpack-ai.git
cd visionpack-ai

Step 2: Create and activate virtual environment
python -m venv venv
venv\Scripts\activate

Step 3: Install dependencies
pip install -r requirements.txt

Step 4: Test YOLOv8 installation
yolo predict model=yolov8n.pt source='https://ultralytics.com/images/bus.jpg'

Step 5: Run the FastAPI backend
uvicorn src.api.main:app --reload --port 8000


Then open 👉 http://127.0.0.1:8000/docs

💬 WhatsApp Feedback Setup

Go to Twilio WhatsApp Sandbox

Join the sandbox by sending your join code (e.g. join is-state) to the Twilio number.

In Sandbox Settings, find “When a message comes in”
and paste your ngrok URL + /feedback endpoint there. Example:

https://your-ngrok-url.ngrok.io/feedback


Now send “yes” or “no” to your Twilio WhatsApp number.

✅ Reply “yes” → confirms detection is correct

❌ Reply “no” → system asks for the correct label

Feedback is saved in data/feedback/log.json.

🔁 Retrain the Model with Feedback

To make your AI smarter using real feedback:

python src/feedback/retrain.py


This retrains the YOLO model using the feedback data you collected.

📊 Streamlit Dashboard

Run this to open the dashboard:

streamlit run src/dashboard/app.py


You can upload images and see the detected objects visually.

💡 Skills Shown in This Project

Object Detection (YOLOv8)

Machine Learning & Model Tuning

API Development (FastAPI)

AI Automation Simulation

WhatsApp API Integration (Twilio)

Data Handling & Retraining

Streamlit Visualization