# src/monitor/performance.py

from __future__ import annotations
import json
import os
import time
from pathlib import Path
from typing import Any, Dict

LOG_DIR = Path("data/logs")
LOG_DIR.mkdir(parents=True, exist_ok=True)
LOG_FILE = LOG_DIR / "inference_metrics.jsonl"


def log_inference(
    *,
    source: str,
    inference_time_ms: float,
    num_detections: int,
    avg_conf: float,
    image_shape: list[int] | tuple[int, ...],
    extra: Dict[str, Any] | None = None,
) -> None:
    """
    Append a single inference record as JSON Lines.
    """
    record: Dict[str, Any] = {
        "ts": time.time(),
        "source": source,
        "inference_time_ms": float(inference_time_ms),
        "num_detections": int(num_detections),
        "avg_conf": float(avg_conf),
        "image_shape": list(image_shape),
    }
    if extra:
        record.update(extra)

    with LOG_FILE.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record) + "\n")
