import pandas as pd
import plotly.express as px

def plot_interactive_line(df: pd.DataFrame, y_col: str, title: str):
    fig = px.line(
        df,
        x="timestamp",
        y=y_col,
        title=title,
        labels={y_col: y_col.replace('_', ' ').title(), 'timestamp': 'Time'},
    )
    fig.update_layout(margin=dict(l=20, r=20, t=40, b=20))
    return fig
