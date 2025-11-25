# src/dashboard/app.py

import streamlit as st
import requests
import pandas as pd
import json
from pathlib import Path

API_BASE = "http://localhost:8000"  # change if deployed


st.set_page_config(page_title="VisionPack AI Dashboard", layout="wide")

st.title("📦 VisionPack AI – Monitoring Dashboard")

tab1, tab2, tab3 = st.tabs(["🔍 Predict", "📊 Quality & Performance", "⚙️ System Status"])

with tab1:
    st.header("Run Prediction on Image")
    uploaded = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])
    if uploaded is not None and st.button("Run Detection"):
        files = {"file": uploaded.getvalue()}
        resp = requests.post(f"{API_BASE}/predict", files=files)
        data = resp.json()
        st.json(data)

with tab2:
    st.header("Quality & Inference Metrics")
    log_file = Path("data/logs/inference_metrics.jsonl")
    if log_file.exists():
        rows = []
        with log_file.open() as f:
            for line in f:
                try:
                    rows.append(json.loads(line))
                except json.JSONDecodeError:
                    continue
        if rows:
            df = pd.DataFrame(rows)
            st.subheader("Recent Inferences")
            st.dataframe(df.tail(50), use_container_width=True)

            if "inference_time_ms" in df.columns:
                st.line_chart(df[["inference_time_ms"]].tail(200))

            if "num_detections" in df.columns:
                st.bar_chart(df[["num_detections"]].tail(200))
    else:
        st.info("No metrics logged yet. Call the /predict API first.")

with tab3:
    st.header("System Status")
    try:
        resp = requests.get(f"{API_BASE}/status")
        st.json(resp.json())
    except Exception as e:
        st.error(f"Could not reach API: {e}")
