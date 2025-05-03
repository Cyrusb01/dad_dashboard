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

    drop_count_col_name = f"drop_count"
    slope_col_name = f"slope"
    resampled = (
    df.set_index(["device_id", "timestamp"])
      .groupby(level="device_id")[drop_count_col_name]
      .resample(interval, level="timestamp")
      .last()
      .dropna()
      .to_frame()
    )

    print(resampled)
    breakpoint()
    resampled[slope_col_name] = np.gradient(resampled[drop_count_col_name])
    df[slope_col_name] = resampled[[slope_col_name]].reindex(df.index, method="bfill")[
        slope_col_name
    ]
    print(df)

    return df
