import pandas as pd

def compute_daily_drop_totals(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["date"] = df["timestamp"].dt.date

    box1 = df[df["device_id"].str.endswith("1")]
    box2 = df[df["device_id"].str.endswith("2")]

    daily_totals = []
    for box_df, label in [(box1, "Box 1"), (box2, "Box 2")]:
        daily = (
            box_df.sort_values("timestamp")
            .groupby("date")["drop_count"]
            .agg(["min", "max"])
            .reset_index()
        )
        daily["device"] = label
        daily["drops"] = daily["max"] - daily["min"]
        daily_totals.append(daily[["date", "device", "drops"]])

    return pd.concat(daily_totals).sort_values("date")
