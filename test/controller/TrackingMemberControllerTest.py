from fastapi.testclient import TestClient

from train.app.application import app

client = TestClient(app)

def test_get_items():
    # basic authentication is required
    token = "cm9ib3Q6cGxheQ=="
    response = client.get("/hello", headers={"Authorization": f"Basic {token}"})
    assert response.status_code == 200
    assert response.json() == []


def test_app_tracking_members():
    response = client.get("/app-tracking-members")
    assert response.status_code == 200
    assert response.json() == []