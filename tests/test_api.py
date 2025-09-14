# tests/test_api.py
from fastapi.testclient import TestClient
from api.main_public import app

def test_health():
    client = TestClient(app)
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"