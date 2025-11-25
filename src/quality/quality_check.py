# src/quality/quality_check.py

from __future__ import annotations
import cv2
import numpy as np
from typing import Dict


def _to_gray(image: np.ndarray) -> np.ndarray:
    """Convert RGB/BGR image to grayscale."""
    if len(image.shape) == 3:
        # Assume RGB, convert to BGR for OpenCV operations if needed
        return cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    return image


def blur_score(image: np.ndarray) -> float:
    """
    Measure blur using variance of Laplacian.
    Higher value = sharper image.
    """
    gray = _to_gray(image)
    lap = cv2.Laplacian(gray, cv2.CV_64F)
    return float(lap.var())


def brightness_score(image: np.ndarray) -> float:
    """
    Approximate brightness in range [0, 1].
    0 = completely dark, 1 = completely white.
    """
    gray = _to_gray(image)
    return float(gray.mean() / 255.0)


def noise_level(image: np.ndarray) -> float:
    """
    Very simple noise estimate: standard deviation of a high-pass filtered image.
    Higher value = more noise.
    """
    gray = _to_gray(image)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    high_freq = gray.astype("float32") - blurred.astype("float32")
    return float(high_freq.std())


def analyze_frame(image: np.ndarray, fps: float | None = None) -> Dict[str, float | bool]:
    """
    Compute quality metrics for a single frame.
    """
    b_score = blur_score(image)
    br_score = brightness_score(image)
    n_level = noise_level(image)

    return {
        "blur_score": b_score,
        "brightness": br_score,
        "noise_level": n_level,
        "frame_rate": float(fps) if fps is not None else None,
        # For a single frame we can't know motion; set to None or False
        "motion_detected": None,
    }
