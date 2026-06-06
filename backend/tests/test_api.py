from fastapi.testclient import TestClient
from main import app
client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"fastapi dziala": True}

def test_get_currencies():
    response = client.get("/currencies")
    assert response.status_code in [200, 400]

def test_fetch_currencies():
    response = client.post("/currencies/fetch")
    assert response.status_code in [200,400]

def test_weekend_error():
    response = client.post("/currencies/fetch?date=2026-01-03")
    assert response.status_code == 400
    assert "Gielda zamknieta w soboty i niedziele" in response.json()["detail"]