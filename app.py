import streamlit as st
from data_loader import process_data
from metrics import calculate_average_external_humidity, calculate_average_external_temperature
from plots import plot_interactive_line
from pathlib import Path

_DATA_PATH = Path("data/data.csv")

st.set_page_config(page_title="Environmental Dashboard", layout="wide")
st.title("Environmental Monitoring Dashboard")

df = process_data(_DATA_PATH)

st.subheader("Average Values")
col1, col2 = st.columns(2)
col1.metric("Average External Humidity (%)", f"{calculate_average_external_humidity(df):.2f}")
col2.metric("Average External Temperature (°F)", f"{calculate_average_external_temperature(df):.2f}")

st.subheader("Time Series Graphs")
col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(plot_interactive_line(df, 'box_1_drop_count', 'Drop Count - Box 1'), use_container_width=True)
with col2:
    st.plotly_chart(plot_interactive_line(df, 'box_2_drop_count', 'Drop Count - Box 2'), use_container_width=True)

col3, col4 = st.columns(2)
with col3:
    st.plotly_chart(plot_interactive_line(df, 'external_humidity', 'External Humidity'), use_container_width=True)
with col4:
    st.plotly_chart(plot_interactive_line(df, 'external_temperature', 'External Temperature'), use_container_width=True)
