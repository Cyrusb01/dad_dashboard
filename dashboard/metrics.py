import pandas as pd
import numpy as np

_DROPS_IN_ML = 20

def calculate_water_per_day(df: pd.DataFrame) -> None:
    df['date'] = df['timestamp'].dt.date
    df['box_1_day_total'] = df.groupby('date')['box_1_drop_count'].transform(lambda x: x.max() - x.min())
    df['box_2_day_total'] = df.groupby('date')['box_2_drop_count'].transform(lambda x: x.max() - x.min())
    df['box_1_day_ml'] = df['box_1_day_total'] * (1/_DROPS_IN_ML)
    df['box_2_day_ml'] = df['box_2_day_total'] * (1/_DROPS_IN_ML)

def calculate_resampled_slopes(df: pd.DataFrame, box_ids: list[int], interval: str = '20min') -> None:
    df.sort_values('timestamp', inplace=True)
    df.set_index('timestamp', inplace=True)

    for box_id in box_ids:
        col_name = f'box_{box_id}_drop_count'
        slope_col = f'box_{box_id}_slope'
        if col_name not in df.columns:
            continue

        resampled = df[col_name].resample(interval).last().dropna().to_frame()
        resampled[slope_col] = np.gradient(resampled[col_name])
        df[slope_col] = resampled[[slope_col]].reindex(df.index, method='ffill')[slope_col]

    df.reset_index(inplace=True)
