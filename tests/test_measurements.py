import pytest
from datetime import datetime


def test_upload_from_device(client):
    payload = {
        "device_name": "Box 1",
        "date": datetime.now().date().isoformat(),
        "time": datetime.now().time().replace(microsecond=0).isoformat(),
        "DHT11 Cold Temp (°F)": 72.5,
        "Cold Humidity (%)": 60.0,
        "DHT11 Hot Temp (°F)": 85.1,
        "Hot Humidity (%)": 50.0,
        "Drop Count": 1234
    }
    response = client.post("/measurements/upload", json=payload)
    assert response.status_code == 200
    assert response.json().get("message") == "Measurement saved"
    assert "id" in response.json()

def test_get_all_measurements(client):
    response = client.get("/measurements")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_latest_measurement(client):
    response = client.get("/measurements/latest")
    assert response.status_code == 200
    latest = response.json()
    assert "device_id" in latest
    assert "timestamp" in latest