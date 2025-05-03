import numpy as np
import pandas as pd

_DROPS_IN_ML = 20

_DROP_COUNT_COL_NAME = "drop_count"
_SLOPE_COL_NAME = f"slope"


def calculate_water_per_day(df: pd.DataFrame) -> None:
    df["date"] = df["timestamp"].dt.date
    df["box_1_day_total"] = df.groupby("date")["box_1_drop_count"].transform(
        lambda x: x.max() - x.min()
    )
    df["box_2_day_total"] = df.groupby("date")["box_2_drop_count"].transform(
        lambda x: x.max() - x.min()
    )
    df["box_1_day_ml"] = df["box_1_day_total"] * (1 / _DROPS_IN_ML)
    df["box_2_day_ml"] = df["box_2_day_total"] * (1 / _DROPS_IN_ML)


def add_resampled_slopes(df: pd.DataFrame, interval: str = "20min") -> pd.DataFrame:
    df = df.copy()
    df = df.sort_values("timestamp")

    # Create multiindex for resampling
    grouped = (
        df.set_index(["device_id", "timestamp"])
        .groupby(level="device_id")[_DROP_COUNT_COL_NAME]
        .resample(interval, level="timestamp")
        .last()
        .dropna()
        .to_frame()
    )

    # Compute slope per device
    grouped[_SLOPE_COL_NAME] = grouped.groupby(level="device_id")[
        _DROP_COUNT_COL_NAME
    ].transform(np.gradient)

    # Flatten back to standard index
    grouped = grouped.reset_index()

    # Merge slope back onto the original dataframe using nearest timestamp within device
    df[_SLOPE_COL_NAME] = pd.merge_asof(
        df.sort_values("timestamp"),
        grouped.sort_values("timestamp"),
        by="device_id",
        on="timestamp",
        direction="backward",
    )[_SLOPE_COL_NAME]
    return df
