import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import date
from collections.abc import Mapping

_BOX_COLORS = [
    "#2A9D8F",
    "#9B5DE5",
    "#F4A261",
    "#264653",
    "#FF6B6B",
]  # green, purple, tan, blue-grey, coral
DROPS_TO_ML = 0.05
_DAYS_FOR_BAR_CHART = 5


def _get_device_name_to_color(df: pd.DataFrame) -> Mapping[str, str]:
    device_names = sorted(df["name"].dropna().unique())
    device_name_to_color = {
        name: color for name, color in zip(device_names, _BOX_COLORS)
    }
    return device_name_to_color


def plot_combined_chart(df: pd.DataFrame, start_date: date = None) -> go.Figure:
    if start_date:
        df = df[df["timestamp"] >= pd.Timestamp(start_date)]
    fig = go.Figure()

    # External Temp and Humidity
    fig.add_trace(
        go.Scatter(
            x=df["timestamp"],
            y=df["temperature"],
            name="Temperature (°F)",
            yaxis="y1",
            line=dict(color="#E63946"),  # Red
        )
    )
    fig.add_trace(
        go.Scatter(
            x=df["timestamp"],
            y=df["humidity"],
            name="Humidity (%)",
            yaxis="y1",
            line=dict(color="#457B9D"),  # Blue
        )
    )
    device_name_to_color = _get_device_name_to_color(df)
    for device_name, color in device_name_to_color.items():
        device_df = df[df["name"] == device_name]
        fig.add_trace(
            go.Scatter(
                x=device_df["timestamp"],
                y=device_df["slope"],
                name=f"{device_name} Slope",
                yaxis="y2",
                line=dict(color=color),
            )
        )
    fig.update_layout(
        title="Environmental & Drop Count Overview",
        xaxis=dict(title="Time"),
        yaxis=dict(title="Temp (°F) / Humidity (%)", range=[0, 110]),
        yaxis2=dict(title="Drop Count Slope", overlaying="y", side="right"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        margin=dict(l=40, r=40, t=40, b=40),
    )
    return fig


def plot_estimated_water_production_per_day(
    df: pd.DataFrame, start_date: date = None
) -> go.Figure:
    df["date"] = df["timestamp"].dt.date
    daily_water = (
        df.sort_values("timestamp")
        .groupby(["device_id", "date"])["drop_count"]
        .agg(["min", "max"])
        .reset_index()
    )
    daily_water["drops"] = daily_water["max"] - daily_water["min"]
    daily_water["estimated_water_ml"] = daily_water["drops"] * DROPS_TO_ML

    name_map = df[["device_id", "name"]].drop_duplicates()
    daily_water = pd.merge(daily_water, name_map, on="device_id", how="left")

    start = pd.to_datetime(start_date).date()
    end = start + pd.Timedelta(days=_DAYS_FOR_BAR_CHART)
    filtered = daily_water[
        (daily_water["date"] >= start) & (daily_water["date"] <= end)
    ]

    device_name_to_color = _get_device_name_to_color(df)
    fig_grouped = px.bar(
        filtered,
        x="date",
        y="estimated_water_ml",
        color="name",
        barmode="group",
        title="Estimated Water Produced Per Day by Device",
        labels={"name": "Device", "estimated_water_ml": "Water (mL)", "date": "Date"},
        color_discrete_map=device_name_to_color,
    )
    return fig_grouped
