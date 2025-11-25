import numpy as np

import src.utils.video as video_mod
from src.utils.video import process_video


class FakeBox:
    def __init__(self):
        self.xyxy = np.array([[0, 0, 10, 10]], dtype="float32")
        self.cls = np.array([0], dtype="float32")
        self.conf = np.array([0.8], dtype="float32")


class FakeResult:
    def __init__(self, boxes):
        self.boxes = boxes


class FakeModel:
    def __init__(self):
        self.names = {0: "object"}

    def predict(self, image, conf=0.4, verbose=False):
        return [FakeResult([FakeBox()])]


class FakeCap:
    def __init__(self, path):
        self.frame_idx = 0

    def get(self, prop):
        # fake fps
        return 25.0

    def read(self):
        if self.frame_idx >= 3:
            return False, None
        self.frame_idx += 1
        frame = np.zeros((64, 64, 3), dtype="uint8")
        return True, frame

    def release(self):
        pass


def test_process_video_with_fake_capture(monkeypatch):
    # monkeypatch VideoCapture so we don't depend on real video bytes
    monkeypatch.setattr(video_mod.cv2, "VideoCapture", FakeCap)

    fake_model = FakeModel()
    summary = process_video(fake_model, b"dummy-video-bytes", conf=0.4, frame_skip=1)

    assert summary["frames_processed"] == 3
    assert summary["total_objects"] == 3
    assert "fps" in summary
    assert isinstance(summary["frames"], list)
    assert len(summary["frames"]) == 3
