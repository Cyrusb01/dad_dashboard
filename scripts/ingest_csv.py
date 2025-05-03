from pathlib import Path
from uuid import UUID, uuid1, uuid4

import pandas as pd
from sqlalchemy.orm import Session

from dashboard.database.db import SessionLocal, init_db
from dashboard.database.models import Device, Measurement, Weather

_DEVICE_UUIDS = {
    "box_1": UUID("8597098d199646918b8491fa05ac514e"),
    "box_2": UUID("a65a939bdc784da28ee3908f2974386f"),
}
_CSV_PATH = Path("csv_data/data_2025-04-04.csv")
_DEVICES = [
    Device(
        device_id=_DEVICE_UUIDS["box_1"],
        name="Box 1",
        location="Test Bench",
        version_num="v1",
    ),
    Device(
        device_id=_DEVICE_UUIDS["box_2"],
        name="Box 2",
        location="Test Bench",
        version_num="v1",
    ),
]


def _select_new_data(session: Session, df: pd.DataFrame) -> pd.DataFrame:
    latest_time = (
        session.query(Measurement.timestamp)
        .order_by(Measurement.timestamp.desc())
        .limit(1)
        .scalar()
    )
    if latest_time is None:
        latest_time = pd.Timestamp("1970-01-01")
    new_data = df[df["timestamp"] > latest_time]
    return new_data


def _load_csv(session: Session, path: Path) -> pd.DataFrame:
    df = pd.read_csv(path)
    df.columns = (
        df.columns.str.strip()
        .str.lower()
        .str.replace(" ", "_")
        .str.replace("(", "")
        .str.replace(")", "")
        .str.replace(".", "")
    )
    df["timestamp"] = pd.to_datetime(df["date"] + " " + df["time"])
    df = df.sort_values("timestamp")
    df = df.drop(columns=["date", "time"])
    df_non_duplicates = _select_new_data(session, df)
    return df_non_duplicates


def _init_devices(session: Session):
    for device in _DEVICES:
        exists = session.query(Device).filter_by(device_id=device.device_id).first()
        if not exists:
            session.add(device)
    session.commit()


def insert_weather(session: Session, row: pd.Series):
    if pd.notnull(row.get("ext_dht11_temp_°f")) or pd.notnull(
        row.get("ext_humidity_%")
    ):
        session.add(
            Weather(
                timestamp=row["timestamp"],
                temperature=row.get("ext_dht11_temp_°f"),
                humidity=row.get("ext_humidity_%"),
            )
        )


def insert_measurement(session: Session, row: pd.Series, device_id: int, prefix: str):
    if pd.notnull(row.get(f"{prefix}_drop_count")):
        session.add(
            Measurement(
                device_id=device_id,
                timestamp=row["timestamp"],
                cold_temp=row.get(f"{prefix}_dht11_cold_temp_°f"),
                cold_humidity=row.get(f"{prefix}_cold_humidity_%"),
                hot_temp=row.get(f"{prefix}_dht11_hot_temp_°f"),
                hot_humidity=row.get(f"{prefix}_hot_humidity_%"),
                drop_count=row.get(f"{prefix}_drop_count"),
            )
        )


def main():
    init_db()
    session = SessionLocal()
    df = _load_csv(session, _CSV_PATH)
    _init_devices(session)

    for _, row in df.iterrows():
        insert_weather(session, row)
        insert_measurement(
            session, row, device_id=_DEVICE_UUIDS["box_1"], prefix="box_1"
        )
        insert_measurement(
            session, row, device_id=_DEVICE_UUIDS["box_2"], prefix="box_2"
        )

    session.commit()
    session.close()
    print(f"Ingested {len(df)} new rows.")


if __name__ == "__main__":
    main()
