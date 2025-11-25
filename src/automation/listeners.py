# src/automation/listeners.py

from __future__ import annotations
from src.automation.event_engine import EventType, register_listener
from src.monitor.performance import log_inference


def register_all_listeners() -> None:
    def on_quality_issue(payload):
        # you can log, send WhatsApp, trigger retrain, etc.
        log_inference(
            source=payload.get("source", "unknown"),
            inference_time_ms=payload.get("runtime_ms", 0.0),
            num_detections=payload.get("num_detections", 0),
            avg_conf=payload.get("avg_conf", 0.0),
            image_shape=payload.get("image_shape", []),
            extra={"quality_issue": True},
        )

    register_listener(EventType.QUALITY_ISSUE, on_quality_issue)
