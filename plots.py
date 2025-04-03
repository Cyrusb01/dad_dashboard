import pandas as pd
import plotly.express as px

def plot_interactive_line(df, y_col, title, start_date=None):
    fig = px.line(df, x='timestamp', y=y_col, title=title)
    if start_date:
        fig.update_xaxes(range=[pd.Timestamp(start_date), df['timestamp'].max()])
    fig.update_layout(margin=dict(l=20, r=20, t=40, b=20))
    return fig
