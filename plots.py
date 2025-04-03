import pandas as pd
import plotly.express as px

def plot_interactive_line(df: pd.DataFrame, y_col: str, title: str, start_date=None):
    fig = px.line(
        df,
        x='timestamp',
        y=y_col,
        title=title,
        labels={y_col: y_col.replace('_', ' ').title(), 'timestamp': 'Time'},
    )
    if start_date:
        fig.update_xaxes(range=[pd.Timestamp(start_date), df['timestamp'].max()])

    y_data = df[y_col]
    y_min = y_data.min()
    y_max = y_data.max()
    padding = (y_max - y_min) * .3 if y_max != y_min else 1
    fig.update_yaxes(range=[y_min - padding, y_max + padding])

    # fig.update_layout(margin=dict(l=20, r=20, t=40, b=20))
    return fig
