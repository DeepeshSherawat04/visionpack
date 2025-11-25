# src/automation/retrainer.py

from __future__ import annotations
from pathlib import Path
from ultralytics import YOLO
import time


FEEDBACK_CORRECT_DIR = Path("data/feedback/correct")
FEEDBACK_WRONG_DIR = Path("data/feedback/wrong")
MODELS_DIR = Path("models")
MODELS_DIR.mkdir(parents=True, exist_ok=True)

MIN_FEEDBACK_IMAGES = 50  # you can tune


def should_retrain() -> bool:
    num_images = 0
    for d in (FEEDBACK_CORRECT_DIR, FEEDBACK_WRONG_DIR):
        if d.exists():
            num_images += len(list(d.glob("*.jpg"))) + len(list(d.glob("*.png")))
    return num_images >= MIN_FEEDBACK_IMAGES


def run_retrain(dataset_yaml: str = "experiments/yolov8/dataset.yaml") -> str:
    """
    Train a new YOLO model using ultralytics and return the path to the new weights.
    """
    model = YOLO("yolov8n.pt")  # or your last best model
    results = model.train(
        data=dataset_yaml,
        epochs=20,
        imgsz=640,
        project="experiments/yolov8",
        name=f"run_{int(time.time())}",
    )
    new_weights = results.best
    # copy to models dir with nicer name
    from shutil import copy2

    target = MODELS_DIR / f"visionpack-{int(time.time())}.pt"
    copy2(new_weights, target)
    return str(target)
