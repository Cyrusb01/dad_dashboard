import uuid
from dashboard.database.models import Device
from dashboard.database.db import SessionLocal, init_db


def setup_test_device(device_name: str) -> uuid.UUID:
    init_db()
    session = SessionLocal()
    device_id = uuid.uuid4()
    device = Device(
        device_id=device_id,
        name=device_name,
        location="Test Bench",
        version_num="v1",
        notes="Test device"
    )
    session.add(device)
    session.commit()
    session.close()
    return device_id
