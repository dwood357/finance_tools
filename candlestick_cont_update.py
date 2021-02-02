import os
import pathlib
import numpy as np
import datetime as dt
import dash
import dash_core_components as dcc
import dash_html_components as html

import pandas as pd
from pandas_datareader import data as source
import plotly.graph_objects as go

from dash.exceptions import PreventUpdate
from dash.dependencies import Input, Output, State


ticker = 'AAPL'
# update = 0

GRAPH_INTERVAL = os.environ.get("GRAPH_INTERVAL", 5000)

app = dash.Dash(
    __name__,
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
)

server = app.server

app_color = {"graph_bg": "#082255", "graph_line": "#007ACE", "page_color": "#696969"}

app.layout = html.Div(
    [
        # header
        html.Div(
            [
                html.Div(
                    [
                        html.H4("{} Candlestick Graph".format(ticker), className="app__header__title"),
                        html.P(
                            "This app continually queries a finance database and displays live charts of Candlestick data.",
                            className="app__header__title--grey",
                        ),
                    ],
                    className="app__header__desc",
                ),
                html.Div(
                    [
                        html.Img(
                            src=app.get_asset_url("dash-new-logo.png"),
                            className="app__menu__img",
                        )
                    ],
                    className="app__header__logo",
                ),
            ],
            className="app__header",
        ),
        html.Div(
            [
                # wind speed
                html.Div(
                    [
                        html.Div(
                            [html.H6("{}".format(ticker), className="graph__title")]
                        ),
                        dcc.Graph(
                            id="finance_data",
                            figure=dict(
                                layout=dict(
                                    plot_bgcolor=app_color["graph_bg"],
                                    paper_bgcolor=app_color["page_color"],
                                )
                            ),
                        ),
                        dcc.Interval(
                            id="finance_data_update",
                            interval=int(GRAPH_INTERVAL),
                            n_intervals=0,
                        ),
                    ],
                    className="graph",
                ),
            ],
            className="app__content",
        ),
    ],
    className="app__container",
)


@app.callback(
    Output("finance_data", "figure"), [Input("finance_data_update", "n_intervals")]
)

def gen_candlestick_data(interval):
    """
    Generate the wind direction graph.
    :params interval: update the graph based on an interval
    """
    # update += 1

    # df = source.DataReader(
    #     ticker, 
    #     data_source='yahoo', 
    #     start='01-11-2021')
    df = source.DataReader(
        ticker, 
        data_source = 'av-intraday', 
        start='01-18-2021',
        pause = 0.5, 
        api_key=os.getenv('ALPHAVANTAGE_API_KEY'))
    # print(df.Close[0])

    trace1 = {
        'x': df.index,
        'open': df.Open,
        'close': df.Close,
        'high': df.High,
        'low': df.Low,
        'type': 'candlestick',
        'name': ticker,
        'showlegend': True
    }

    # Calculate and define moving average of 30 periods
    avg_30 = df.Close.rolling(window=30, min_periods=1).mean()

    # Calculate and define moving average of 50 periods
    avg_50 = df.Close.rolling(window=50, min_periods=1).mean()

    trace2 = {
        'x': df.index,
        'y': avg_30,
        'type': 'scatter',
        'mode': 'lines',
        'line': {
            'width': 1,
            'color': 'blue'
                },
        'name': 'Moving Average of 30 periods'
    }

    trace3 = {
        'x': df.index,
        'y': avg_50,
        'type': 'scatter',
        'mode': 'lines',
        'line': {
            'width': 1,
            'color': 'red'
        },
        'name': 'Moving Average of 50 periods'
    }

    data = [trace1, trace2, trace3]
    # Config graph layout
    layout = go.Layout({
        'title': {
            'text': '{} Moving Averages'.format(ticker),
            'font': {
                'size': 15
            }
        }
    })



    return dict(data=data, layout=layout)



if __name__ == "__main__":
    app.run_server(debug=True, host = '127.0.0.1',port = '8051')