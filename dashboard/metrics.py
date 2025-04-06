import numpy as np
import pandas as pd

_DROPS_IN_ML = 20


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


def add_resampled_slopes(
    df: pd.DataFrame, interval: str = "20min"
) -> None:
    



    df.sort_values("timestamp", inplace=True)
    df.set_index("timestamp", inplace=True)

    col_name = f"drop_count"
    slope_col = f"slope"
    resampled = (
    df.set_index(["device_id", "timestamp"])
      .groupby(level="device_id")[col_name]
      .resample(interval, level="timestamp")
      .last()
      .dropna()
      .to_frame()
)
    resampled[slope_col] = np.gradient(resampled[col_name])
    df[slope_col] = resampled[[slope_col]].reindex(df.index, method="ffill")[
        slope_col
    ]

df.reset_index(inplace=True)
