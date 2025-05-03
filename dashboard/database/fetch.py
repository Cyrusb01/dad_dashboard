import pandas as pd
from sqlalchemy.orm import Session

from dashboard.database.db import SessionLocal
from dashboard.database.models import Device, Measurement, Weather


def _fetch_measurements(session:Session) -> pd.DataFrame:
    rows = session.query(Measurement).all()
    df = pd.DataFrame(
        [
            {
                "timestamp": row.timestamp,
                "device_id": str(row.device_id),
                "cold_temp": row.cold_temp,
                "cold_humidity": row.cold_humidity,
                "hot_temp": row.hot_temp,
                "hot_humidity": row.hot_humidity,
                "drop_count": row.drop_count,
            }
            for row in rows
        ]
    )
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    return df

def _fetch_devices(session: Session) -> pd.DataFrame:
    rows = session.query(Device).all()
    df = pd.DataFrame(
        [
            {
                "device_id": str(row.device_id),
                "name": row.name,
                "location": row.location,
                "version_num": row.version_num,
                "notes": row.notes,
            }
            for row in rows
        ]
    )
    return df

def _fetch_weather(session: Session)-> pd.DataFrame:
    rows = session.query(Weather).all()
    df = pd.DataFrame(
        [
            {
                "timestamp": row.timestamp,
                "temperature": row.temperature,
                "humidity": row.humidity,
            }
            for row in rows
        ]
    )
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    return df

def get_all_data()->pd.DataFrame:
    session = SessionLocal()
    try:
        measurements = _fetch_measurements(session)
        weather = _fetch_weather(session)
        devices = _fetch_devices(session)
        breakpoint()
        measurements_and_weather = pd.merge(weather, measurements, on="timestamp", how="left")
        measurements_weather_and_devices = measurements_and_weather.join(devices, on="device_id", how="left")
        return measurements_weather_and_devices
    finally:
        session.close()
