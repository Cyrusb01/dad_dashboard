# 🌿 Dad's Dashboard API Guide

This guide shows how to send data from your device to our dashboard system.

---

## ✅ API Base URL

Coming Soon

## 📦 1. Uploading Box Measurements

Measurement data is device specifc (Box 1, Box 2)

### 🔁 Endpoint:
```
POST /measurements/upload
```

### 🧾 Example Payload:
```json
{
  "device_name": "Box 1",
  "date": "2025-04-06",
  "time": "14:30:00",
  "DHT11 Cold Temp (°F)": 72.5,
  "Cold Humidity (%)": 60.2,
  "DHT11 Hot Temp (°F)": 80.3,
  "Hot Humidity (%)": 50.4,
  "Drop Count": 120
}
```

Make sure to match the key names exactly (with spaces and symbols).\
The names can be changed let me know if you want that. \
For now `device_name` should be "Box 1" or "Box 2"

---

## 🌤️ 2. Uploading Weather Data

External Weather Data from Data Logger

### 🔁 Endpoint:
```
POST /weather/upload
```

### 🧾 Example Payload:
```json
{
  "date": "2025-04-06",
  "time": "14:30:00",
  "Ext. DHT11 Temp (°F)": 71.1,
  "Ext. Humidity (%)": 54.8
}
```
