"""
Benchmark script for VisionPack AI.

Usage:
    python -m scripts.benchmark --image bus.jpg --iterations 50
"""

import argparse
import time
from pathlib import Path

import numpy as np
from PIL import Image
from ultralytics import YOLO


def run_benchmark(model_path: str, image_path: str, iterations: int = 50):
    model = YOLO(model_path)

    img = Image.open(image_path).convert("RGB")
    img_np = np.array(img)

    # warm-up
    _ = model.predict(img_np, conf=0.4)

    times = []
    for _ in range(iterations):
        t0 = time.perf_counter()
        _ = model.predict(img_np, conf=0.4)
        t1 = time.perf_counter()
        times.append((t1 - t0) * 1000.0)  # ms

    avg_ms = sum(times) / len(times)
    fps = 1000.0 / avg_ms if avg_ms > 0 else 0.0

    print(f"Model: {model_path}")
    print(f"Image: {image_path}")
    print(f"Iterations: {iterations}")
    print(f"Average latency: {avg_ms:.2f} ms")
    print(f"Approx FPS: {fps:.2f}")


def parse_args():
    parser = argparse.ArgumentParser(description="Benchmark YOLO inference speed.")
    parser.add_argument(
        "--model",
        type=str,
        default="yolov8n.pt",
        help="Path to YOLO model weights",
    )
    parser.add_argument(
        "--image",
        type=str,
        default="bus.jpg",
        help="Path to test image",
    )
    parser.add_argument(
        "--iterations",
        type=int,
        default=50,
        help="Number of inference iterations",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    image_path = Path(args.image)
    if not image_path.exists():
        raise SystemExit(f"Image not found: {image_path}")

    run_benchmark(args.model, str(image_path), iterations=args.iterations)
