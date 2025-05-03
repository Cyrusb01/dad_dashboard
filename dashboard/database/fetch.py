import pandas as pd
from sqlalchemy.orm import Session

from dashboard.database.db import SessionLocal
from dashboard.database.models import Device, Measurement, Weather


def _fetch_measurements(session: Session) -> pd.DataFrame:
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
    df = df.astype(
        {
            "timestamp": "datetime64[ns]",
            "device_id": "string",
            "cold_temp": "float",
            "cold_humidity": "float",
            "hot_temp": "float",
            "hot_humidity": "float",
            "drop_count": "Int64",  # capital 'I' for nullable ints
        }
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
    df = df.astype(
        {
            "device_id": "string",
            "name": "string",
            "location": "string",
            "version_num": "string",
            "notes": "string",
        }
    )
    return df


def _fetch_weather(session: Session) -> pd.DataFrame:
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
    df = df.astype(
        {
            "timestamp": "datetime64[ns]",
            "temperature": "float",
            "humidity": "float",
        }
    )
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    return df


def get_all_data() -> pd.DataFrame:
    session = SessionLocal()
    try:
        measurements = _fetch_measurements(session)
        weather = _fetch_weather(session)
        devices = _fetch_devices(session)
        measurements_and_weather = pd.merge(
            weather, measurements, on="timestamp", how="left"
        )
        measurements_weather_and_devices = pd.merge(
            measurements_and_weather, devices, on="device_id", how="left"
        )
        return measurements_weather_and_devices
    finally:
        session.close()
