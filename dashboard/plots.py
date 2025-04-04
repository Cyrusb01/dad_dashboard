import pandas as pd
import plotly.graph_objects as go

def plot_combined_chart(df: pd.DataFrame, start_date=None):
    if start_date:
        df = df[df['timestamp'] >= pd.Timestamp(start_date)]

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=df['timestamp'], y=df['external_temperature'],
        name='Temperature (°F)',
        yaxis='y1',
        line=dict(color='#E63946')  # Red
    ))

    fig.add_trace(go.Scatter(
        x=df['timestamp'], y=df['external_humidity'],
        name='Humidity (%)',
        yaxis='y1',
        line=dict(color='#457B9D')  # Blue
    ))

    fig.add_trace(go.Scatter(
        x=df['timestamp'], y=df['box_1_slope'],
        name='Box 1 Drop Count',
        yaxis='y2',
        line=dict(color='#2A9D8F')  # green
    ))

    fig.add_trace(go.Scatter(
        x=df['timestamp'], y=df['box_2_slope'],
        name='Box 2 Drop Count',
        yaxis='y2',
        line=dict(color='#9B5DE5')  # purple
    ))

    fig.update_layout(
        title='Environmental & Drop Count Overview',
        xaxis=dict(title='Time'),
        yaxis=dict(
            title='Temp (°F) / Humidity (%)',
            range=[0, 110]
        ),
        yaxis2=dict(
            title='Drop Count',
            overlaying='y',
            side='right'
        ),
        legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1),
        margin=dict(l=40, r=40, t=40, b=40)
    )

    return fig