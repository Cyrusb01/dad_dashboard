from pathlib import Path

import plotly.express as px
import streamlit as st

from dashboard.plots import plot_combined_chart, plot_estimated_water_production_per_day
from dashboard.database.fetch import get_all_data
import pandas as pd
from metrics import add_resampled_slopes
from datetime import date


def _plot_date_selector_and_metrics(df: pd.DataFrame, selected_date: date) -> None:
    df_day = df[df["timestamp"].dt.date == selected_date]
    col1, col2 = st.columns(2)
    col1.metric(
        f"Avg Ext. Humidity ({selected_date})",
        f"{df_day['humidity'].mean():.2f}" if not df_day.empty else "N/A",
    )
    col2.metric(
        f"Avg Ext. Temp ({selected_date})",
        f"{df_day['temperature'].mean():.2f}" if not df_day.empty else "N/A",
    )
    return


def _plot_drop_production_chart(df: pd.DataFrame, selected_date: date) -> None:
    drop_production_df = df.copy()
    df_with_resampled_slopes = add_resampled_slopes(drop_production_df)

    st.subheader("Time Series Charts")
    st.plotly_chart(
        plot_combined_chart(df_with_resampled_slopes, selected_date),
        use_container_width=True,
    )


st.set_page_config(page_title="Environmental Dashboard", layout="wide")
st.title("Environmental Monitoring Dashboard")

df = get_all_data()

selected_date = st.date_input("Select a date", value=df["timestamp"].dt.date.min())

_plot_date_selector_and_metrics(df, selected_date)
_plot_drop_production_chart(df, selected_date)


# Additional Insights
st.subheader("Additional Insights")

estimated_water_production_per_day_chart = plot_estimated_water_production_per_day(
    df, selected_date
)
st.plotly_chart(estimated_water_production_per_day_chart, use_container_width=True)

# 2. Drop Count by Hour of Day
# if not df_day.empty:
#     df_day["hour"] = df_day["timestamp"].dt.hour
#     df_day["total_drops"] = df_day["box_1_drop_count"] + df_day["box_2_drop_count"]
#     drops_by_hour = df_day.groupby("hour")["total_drops"].sum().reset_index()
#     fig_hourly = px.bar(
#         drops_by_hour,
#         x="hour",
#         y="total_drops",
#         title="Drop Count by Hour (Selected Day)",
#     )
#     st.plotly_chart(fig_hourly, use_container_width=True)
