from .get_data import *
import plotly.graph_objects as go


def dataframe_px(data: pd.DataFrame):
    fig = go.Figure(data=[go.Table(
        columnorder=[1, 2, 3],
        columnwidth=[200, 300, 900],
        header=dict(
            values=[['Username'], ['Type'],
                    ['Content']],
            line_color='darkslategray',
            fill_color='royalblue',
            align=['left', 'center'],
            font=dict(color='white', size=12),
            height=40
        ),
        cells=dict(
            values=[data.username.tolist(), data.referenced_tweets.tolist(), data.text.tolist()],
            line_color='darkslategray',
            fill=dict(color=['paleturquoise', 'white']),
            align=['left', 'center'],
            font_size=12,
            height=30)
    )
    ])
    return fig
