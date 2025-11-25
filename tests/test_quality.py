# tests/test_quality.py

import numpy as np
from src.quality.quality_check import analyze_frame


def test_analyze_frame_returns_keys():
    """
    Verify that analyze_frame() returns all expected keys.
    """
    img = np.zeros((256, 256, 3), dtype="uint8")
    result = analyze_frame(img)

    required_keys = [
        "blur_score",
        "brightness",
        "noise_level",
        "frame_rate",
        "motion_detected",
    ]

    for key in required_keys:
        assert key in result, f"Missing key: {key}"


def test_analyze_frame_value_types():
    """
    Check that the values have correct data types.
    """
    img = np.random.randint(0, 255, (128, 128, 3), dtype="uint8")
    result = analyze_frame(img)

    assert isinstance(result["blur_score"], (int, float))
    assert isinstance(result["brightness"], float)
    assert isinstance(result["noise_level"], float)
    assert result["frame_rate"] is None or isinstance(result["frame_rate"], float)
    # motion_detected may be None or bool
    assert isinstance(result["motion_detected"], (bool, type(None)))
