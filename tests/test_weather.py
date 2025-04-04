from datetime import datetime


def test_upload_weather(client):
    payload = {
        "date": datetime.now().date().isoformat(),
        "time": datetime.now().time().replace(microsecond=0).isoformat(),
        "Ext. DHT11 Temp (°F)": 70.5,
        "Ext. Humidity (%)": 55.0
    }
    response = client.post("/weather/upload", json=payload)
    assert response.status_code == 200
    assert response.json().get("message") == "Weather saved"
    assert "timestamp" in response.json()


def test_get_all_weather(client):
    response = client.get("/weather")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_latest_weather(client):
    response = client.get("/weather/latest")
    assert response.status_code == 200
    latest = response.json()
    assert "temperature" in latest
    assert "humidity" in latest
    assert "timestamp" in latest
