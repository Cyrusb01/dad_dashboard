import uuid

from sqlalchemy import (TIMESTAMP, Column, Float, ForeignKey, Integer, String,
                        Text, func)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Device(Base):
    __tablename__ = "devices"

    device_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    location = Column(Text)
    version_num = Column(String)
    notes = Column(Text)
    created_at = Column(TIMESTAMP, server_default=func.now())


class Measurement(Base):
    __tablename__ = "measurements"

    measurement_id = Column(Integer, primary_key=True, autoincrement=True)
    device_id = Column(
        UUID(as_uuid=True), ForeignKey("devices.device_id"), nullable=False
    )
    timestamp = Column(TIMESTAMP, nullable=False)
    cold_temp = Column(Float)
    cold_humidity = Column(Float)
    hot_temp = Column(Float)
    hot_humidity = Column(Float)
    drop_count = Column(Integer)
    created_at = Column(TIMESTAMP, server_default=func.now())


class Weather(Base):
    __tablename__ = "weather"

    timestamp = Column(TIMESTAMP, primary_key=True)
    temperature = Column(Float)
    humidity = Column(Float)
    created_at = Column(TIMESTAMP, server_default=func.now())
