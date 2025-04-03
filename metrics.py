import pandas as pd

def calculate_average_external_humidity(df: pd.DataFrame) -> float:
    return df['external_humidity'].mean()

def calculate_average_external_temperature(df: pd.DataFrame) -> float:
    return df['external_temperature'].mean()
