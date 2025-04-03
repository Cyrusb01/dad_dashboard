import pandas as pd
from pathlib import Path

def process_data(csv_path: Path) -> pd.DataFrame:
    df = pd.read_csv(csv_path)
    df['timestamp'] = pd.to_datetime(df['Date'] + ' ' + df['Time'])
    df = df.sort_values('timestamp')
    df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_').str.replace('(', '').str.replace(')', '').str.replace('.', '')
    df.rename(columns={
        'ext_dht11_temp_°f': 'external_temperature',
        'ext_humidity_%': 'external_humidity',
        'ext_dew_point_°f': 'external_dew_point'
    }, inplace=True)
    df = df.drop(columns=["date", "time"])
    return df


print(process_data("data/data.csv"))