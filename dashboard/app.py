import streamlit as st
from data_loader import process_data
from dashboard.plots import plot_combined_chart
from pathlib import Path
import plotly.express as px

_DATA_PATH = Path("data/data.csv")

st.set_page_config(page_title="Environmental Dashboard", layout="wide")
st.title("Environmental Monitoring Dashboard")

df = process_data(_DATA_PATH)

selected_date = st.date_input("Select a date", value=df['timestamp'].dt.date.min())
df_day = df[df['timestamp'].dt.date == selected_date]


col3, col4 = st.columns(2)
col3.metric(
    f"Avg Ext. Humidity ({selected_date})",
    f"{df_day['external_humidity'].mean():.2f}" if not df_day.empty else "N/A"
)
col4.metric(
    f"Avg Ext. Temp ({selected_date})",
    f"{df_day['external_temperature'].mean():.2f}" if not df_day.empty else "N/A"
)

st.subheader("Time Series Charts")
st.plotly_chart(plot_combined_chart(df, selected_date), use_container_width=True)

# Additional Insights
st.subheader("Additional Insights")

# 1. Estimated Water Production (assume 1 drop = 0.05 mL)
df['total_drops'] = df['box_1_drop_count'] + df['box_2_drop_count']
df['estimated_water_ml'] = df['total_drops'] * 0.05

water_per_day = df.groupby(df['timestamp'].dt.date)['estimated_water_ml'].sum().reset_index()
water_per_day.columns = ['date', 'estimated_water_ml']
fig_water = px.bar(water_per_day, x='date', y='estimated_water_ml', title='Estimated Water Produced Per Day (mL)')
st.plotly_chart(fig_water, use_container_width=True)

# 2. Drop Count by Hour of Day
if not df_day.empty:
    df_day['hour'] = df_day['timestamp'].dt.hour
    df_day['total_drops'] = df_day['box_1_drop_count'] + df_day['box_2_drop_count']
    drops_by_hour = df_day.groupby('hour')['total_drops'].sum().reset_index()
    fig_hourly = px.bar(drops_by_hour, x='hour', y='total_drops', title='Drop Count by Hour (Selected Day)')
    st.plotly_chart(fig_hourly, use_container_width=True)