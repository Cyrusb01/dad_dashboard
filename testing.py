from dashboard.database.fetch import get_all_data
from dashboard.metrics import add_resampled_slopes
import pandas as pd

df = get_all_data()
add_resampled_slopes(df)
