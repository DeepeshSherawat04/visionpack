from fastapi.testclient import TestClient
import src.api.main as api_main


client = TestClient(api_main.app)


def test_status_endpoint_basic():
    resp = client.get("/status")
    assert resp.status_code == 200

    data = resp.json()
    assert data["status"] == "ok"
    assert "uptime_seconds" in data
    assert data["model_loaded"] is True
