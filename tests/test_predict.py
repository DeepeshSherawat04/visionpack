# visionpack-ai/tests/test_predict.py

import io
from fastapi.testclient import TestClient
from PIL import Image
import src.api.main as api_main
from src.utils.cache import prediction_cache    # <-- important fix


class FakeBox:
    def __init__(self, x1, y1, x2, y2, cls_idx, conf):
        import numpy as np
        self.xyxy = np.array([[x1, y1, x2, y2]], dtype="float32")
        self.cls = np.array([cls_idx], dtype="float32")
        self.conf = np.array([conf], dtype="float32")


class FakeResult:
    def __init__(self, boxes):
        self.boxes = boxes


class FakeModel:
    def __init__(self):
        self.names = {0: "box"}

    def predict(self, image, conf=0.4):
        box = FakeBox(10, 20, 30, 40, 0, 0.9)
        return [FakeResult([box])]


client = TestClient(api_main.app)


def _make_image_bytes():
    """Create a simple black JPEG image in-memory."""
    img = Image.new("RGB", (64, 64), color="black")
    buf = io.BytesIO()
    img.save(buf, format="JPEG")
    buf.seek(0)
    return buf.getvalue()


def test_predict_returns_detections_and_quality(monkeypatch):
    # Reset global cache to avoid leaking state between tests
    prediction_cache._store.clear()

    fake_model = FakeModel()
    monkeypatch.setattr(api_main, "model", fake_model)

    img_bytes = _make_image_bytes()
    files = {"file": ("test.jpg", img_bytes, "image/jpeg")}

    resp = client.post("/predict", files=files)
    assert resp.status_code == 200

    data = resp.json()
    assert "detections" in data
    assert "quality" in data
    assert "runtime_ms" in data
    assert "cached" in data

    assert isinstance(data["detections"], list)
    assert len(data["detections"]) == 1

    det = data["detections"][0]
    assert det["class"] == "box"
    assert det["conf"] > 0
    assert len(det["bbox"]) == 4

    quality = data["quality"]
    for k in ["blur_score", "brightness", "noise_level", "frame_rate", "motion_detected"]:
        assert k in quality


def test_predict_uses_cache_on_second_call(monkeypatch):
    # Reset cache to ensure test isolation
    prediction_cache._store.clear()

    fake_model = FakeModel()
    monkeypatch.setattr(api_main, "model", fake_model)

    img_bytes = _make_image_bytes()
    files = {"file": ("test.jpg", img_bytes, "image/jpeg")}

    # 1st call – not cached
    resp1 = client.post("/predict", files=files)
    assert resp1.status_code == 200
    assert resp1.json()["cached"] is False

    # 2nd call – should hit cache
    resp2 = client.post("/predict", files=files)
    assert resp2.status_code == 200
    assert resp2.json()["cached"] is True
