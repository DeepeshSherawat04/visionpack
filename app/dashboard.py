# app/dashboard.py
import streamlit as st
from ultralytics import YOLO
from PIL import Image
import numpy as np
import io
import os

st.set_page_config(page_title="VisionPack AI Dashboard", page_icon="🤖", layout="wide")

# Header
st.title("🎯 VisionPack AI – Smart Packaging Detection")
st.write("Upload a packaging image to detect items using YOLOv8 model.")

# Load YOLO model
model_path = "experiments/yolov8/best.pt"
if not os.path.exists(model_path):
    st.error("Model file not found! Please train or copy best.pt into experiments/yolov8/")
    st.stop()

model = YOLO(model_path)

# Upload image
uploaded_file = st.file_uploader("📸 Upload Image", type=["jpg", "jpeg", "png"])

if uploaded_file:
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, caption="Uploaded Image", use_container_width=True)

    # Run YOLO prediction
    with st.spinner("Running detection..."):
        results = model.predict(np.array(image), conf=0.4)

    # Plot detections
    result_image = results[0].plot()  # Draw boxes on image
    st.image(result_image, caption="Detection Results", use_container_width=True)

    # Detection summary
    st.subheader("📊 Detected Objects")
    for box in results[0].boxes:
        st.write({
            "class": model.names[int(box.cls[0])],
            "confidence": float(box.conf[0]),
        })

    # Optional feedback link
    st.info("💬 Provide feedback via WhatsApp for continuous model improvement.")
