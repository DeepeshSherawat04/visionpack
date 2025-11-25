import json
from src.monitor import performance


def test_log_inference_writes_json_line(tmp_path, monkeypatch):
    # redirect log file to a temporary location
    tmp_log = tmp_path / "metrics.jsonl"
    monkeypatch.setattr(performance, "LOG_FILE", tmp_log)

    performance.log_inference(
        source="test",
        inference_time_ms=12.3,
        num_detections=2,
        avg_conf=0.8,
        image_shape=[256, 256, 3],
    )

    assert tmp_log.exists()
    content = tmp_log.read_text().strip()
    lines = content.splitlines()
    assert len(lines) == 1

    data = json.loads(lines[0])
    assert data["source"] == "test"
    assert data["num_detections"] == 2
    assert data["avg_conf"] == 0.8
