from pathlib import Path

import plotly.express as px
import streamlit as st

from dashboard.plots import plot_combined_chart
from data_loader import process_data
from dashboard.database.fetch import get_all_data
import pandas as pd
from metrics import add_resampled_slopes
from datetime import date

def _plot_date_selector_and_metrics(df:pd.DataFrame, selected_date:date)->None:
    df_day = df[df["timestamp"].dt.date == selected_date]
    col1, col2 = st.columns(2)
    col1.metric(
        f"Avg Ext. Humidity ({selected_date})",
        f"{df_day['external_humidity'].mean():.2f}" if not df_day.empty else "N/A",
    )
    col2.metric(
        f"Avg Ext. Temp ({selected_date})",
        f"{df_day['external_temperature'].mean():.2f}" if not df_day.empty else "N/A",
    )
    return

def _plot_drop_production_chart(df:pd.DataFrame, selected_date:date)->None:
    drop_production_df = df.copy()
    add_resampled_slopes(drop_production_df)

    st.subheader("Time Series Charts")
    st.plotly_chart(plot_combined_chart(drop_production_df, selected_date), use_container_width=True)


st.set_page_config(page_title="Environmental Dashboard", layout="wide")
st.title("Environmental Monitoring Dashboard")

df = get_all_data()

selected_date = st.date_input("Select a date", value=df["timestamp"].dt.date.min())

_plot_date_selector_and_metrics()
_plot_drop_production_chart()




# Additional Insights
st.subheader("Additional Insights")

# 1. Estimated Water Production (assume 1 drop = 0.05 mL)
df["total_drops"] = df["box_1_drop_count"] + df["box_2_drop_count"]
df["estimated_water_ml"] = df["total_drops"] * 0.05

water_per_day = (
    df.groupby(df["timestamp"].dt.date)["estimated_water_ml"].sum().reset_index()
)
water_per_day.columns = ["date", "estimated_water_ml"]
fig_water = px.bar(
    water_per_day,
    x="date",
    y="estimated_water_ml",
    title="Estimated Water Produced Per Day (mL)",
)
st.plotly_chart(fig_water, use_container_width=True)

# 2. Drop Count by Hour of Day
if not df_day.empty:
    df_day["hour"] = df_day["timestamp"].dt.hour
    df_day["total_drops"] = df_day["box_1_drop_count"] + df_day["box_2_drop_count"]
    drops_by_hour = df_day.groupby("hour")["total_drops"].sum().reset_index()
    fig_hourly = px.bar(
        drops_by_hour,
        x="hour",
        y="total_drops",
        title="Drop Count by Hour (Selected Day)",
    )
    st.plotly_chart(fig_hourly, use_container_width=True)
