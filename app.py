import streamlit as st
from data_loader import process_data
from metrics import calculate_average_external_humidity, calculate_average_external_temperature
from plots import plot_interactive_line
from pathlib import Path

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
col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(plot_interactive_line(df, 'box_1_drop_count', 'Drop Count – Box 1', selected_date), use_container_width=True)
with col2:
    st.plotly_chart(plot_interactive_line(df, 'box_2_drop_count', 'Drop Count – Box 2', selected_date), use_container_width=True)

col3, col4 = st.columns(2)
with col3:
    st.plotly_chart(plot_interactive_line(df, 'external_humidity', 'External Humidity', selected_date), use_container_width=True)
with col4:
    st.plotly_chart(plot_interactive_line(df, 'external_temperature', 'External Temperature', selected_date), use_container_width=True)