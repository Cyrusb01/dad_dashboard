from fastapi import APIRouter, Depends
from pydantic import BaseModel
from dashboard.database.db import SessionLocal
from dashboard.database.models import Measurement, Device
from sqlalchemy.orm import Session
from uuid import UUID
from datetime import datetime
from typing import Optional, List

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class MeasurementIn(BaseModel):
    device_id: UUID
    timestamp: datetime
    cold_temp: Optional[float] = None
    cold_humidity: Optional[float] = None
    hot_temp: Optional[float] = None
    hot_humidity: Optional[float] = None
    drop_count: Optional[int] = None


class MeasurementOut(BaseModel):
    device_id: UUID
    timestamp: datetime
    cold_temp: Optional[float]
    cold_humidity: Optional[float]
    hot_temp: Optional[float]
    hot_humidity: Optional[float]
    drop_count: Optional[int]

    class Config:
        orm_mode = True


@router.post("/")
def create_measurement(payload: MeasurementIn, db: Session = Depends(get_db)):
    measurement = Measurement(**payload.model_dump())
    db.add(measurement)
    db.commit()
    db.refresh(measurement)
    return {"message": "Measurement saved", "id": measurement.measurement_id}


def _normalize_payload(data: dict, db: Session) -> MeasurementIn:
    device = db.query(Device).filter(Device.name == data.get("device_name")).first()
    if not device:
        raise ValueError(f"Device not found for name: {data.get('device_name')}")

    mapped = {
        "device_id": device.device_id,
        "timestamp": datetime.fromisoformat(f"{data['date']}T{data['time']}"),
        "cold_temp": data.get("DHT11 Cold Temp (°F)"),
        "cold_humidity": data.get("Cold Humidity (%)"),
        "hot_temp": data.get("DHT11 Hot Temp (°F)"),
        "hot_humidity": data.get("Hot Humidity (%)"),
        "drop_count": data.get("Drop Count")
    }
    payload = MeasurementIn(**mapped)
    return payload


@router.post("/upload")
def upload_from_device(raw_data: dict, db: Session = Depends(get_db)):
    try:
        payload = _normalize_payload(raw_data, db)
        return create_measurement(payload, db)
    except Exception as e:
        return {"error": str(e)}


@router.get("/", response_model=List[MeasurementOut])
def get_all_measurements(db: Session = Depends(get_db)):
    return db.query(Measurement).order_by(Measurement.timestamp).all()


@router.get("/latest", response_model=MeasurementOut)
def get_latest_measurement(db: Session = Depends(get_db)):
    return db.query(Measurement).order_by(Measurement.timestamp.desc()).first()
