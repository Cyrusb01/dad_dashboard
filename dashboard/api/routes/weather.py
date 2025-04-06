from datetime import datetime
from typing import List, Optional

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from dashboard.database.db import SessionLocal
from dashboard.database.models import Weather

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class WeatherIn(BaseModel):
    timestamp: datetime
    temperature: Optional[float] = None
    humidity: Optional[float] = None


class WeatherOut(BaseModel):
    timestamp: datetime
    temperature: Optional[float]
    humidity: Optional[float]

    class Config:
        orm_mode = True


@router.post("/")
def create_weather(payload: WeatherIn, db: Session = Depends(get_db)):
    weather = Weather(**payload.model_dump())
    db.add(weather)
    db.commit()
    db.refresh(weather)
    return {"message": "Weather saved", "timestamp": weather.timestamp}


def _normalize_payload(data: dict) -> WeatherIn:
    mapped = {
        "timestamp": datetime.fromisoformat(f"{data['date']}T{data['time']}"),
        "temperature": data.get("Ext. DHT11 Temp (°F)"),
        "humidity": data.get("Ext. Humidity (%)"),
    }
    payload = WeatherIn(**mapped)
    return payload


@router.post("/upload")
def upload_weather(raw_data: dict, db: Session = Depends(get_db)):
    try:
        payload = _normalize_payload(raw_data)
        return create_weather(payload, db)
    except Exception as e:
        return {"error": str(e)}


@router.get("/", response_model=List[WeatherOut])
def get_all_weather(db: Session = Depends(get_db)):
    return db.query(Weather).order_by(Weather.timestamp).all()


@router.get("/latest", response_model=WeatherOut)
def get_latest_weather(db: Session = Depends(get_db)):
    return db.query(Weather).order_by(Weather.timestamp.desc()).first()
