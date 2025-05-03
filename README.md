# 🌱 Dad's Environmental Dashboard

This project is a full-stack dashboard to visualize and monitor environmental data collected by air-to-water plant irrigation devices. It supports real-time ingestion from devices, storage in a structured database, and rich interactive visualizations.

---

## 📦 Project Overview

The project consists of three main components:

- **Dashboard (Streamlit):** Interactive visual frontend displaying temperature, humidity, and water production trends
- **Backend (FastAPI):** REST API for posting measurements and weather data from devices
- **Database (SQLite/PostgreSQL):** Stores device metadata, environmental readings, and external weather overlays

Supporting modules handle data fetching, transformation, plotting, and ingestion from CSV files.

---

## 🚀 How to Run

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Start the FastAPI server (optional)
```bash
uvicorn api.main:app --reload
```

### 3. Launch the Streamlit dashboard
```bash
streamlit run dashboard/app.py
```

---

## 🛰️ API Documentation

See: [`api_documentation.md`](api_documentation.md)

---

## 📊 Dashboard Features

- **Combined Line Chart:** Temperature, humidity, and drop rate over time
- **Daily Water Bar Chart:** Water production per device over a 5-day range
- **Device Color Matching:** Consistent styling across charts
- **Date Selector:** Filter charts starting from a specific date

---

## 🧪 Testing

Run tests with:
```bash
pytest
```
Uses SQLite and FastAPI's test client with isolated sessions.

