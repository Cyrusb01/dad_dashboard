import pandas as pd
from pathlib import Path
import numpy as np
from dashboard.metrics import calculate_resampled_slopes, calculate_water_per_day


def _canonicalize_columns(df:pd.DataFrame)->pd.DataFrame:
    df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_').str.replace('(', '').str.replace(')', '').str.replace('.', '')
    df.rename(columns={
        'ext_dht11_temp_°f': 'external_temperature',
        'ext_humidity_%': 'external_humidity',
        'ext_dew_point_°f': 'external_dew_point'
    }, inplace=True)

def _get_df_with_cleaned_dates(csv_path:Path)->pd.DataFrame:
    df = pd.read_csv(csv_path)
    df['timestamp'] = pd.to_datetime(df['Date'] + ' ' + df['Time'])
    df['timestamp_minute'] = df['timestamp'].dt.floor('min')
    df = df.sort_values('timestamp').groupby('timestamp_minute').last().reset_index()
    df['timestamp'] = df['timestamp_minute']
    df = df.drop(columns=["Date", "Time"])
    return df


def process_data(csv_path: Path) -> pd.DataFrame:
    df = _get_df_with_cleaned_dates(csv_path)
    _canonicalize_columns(df)
    calculate_resampled_slopes(df, [1, 2])
    calculate_water_per_day
    return df
