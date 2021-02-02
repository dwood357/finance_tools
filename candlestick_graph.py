import pandas as pd
from pandas_datareader import data as source
import plotly.graph_objects as go

ticker = 'MSFT'
ticker = 'GME'
ticker = 'AAPL'
 
tickers = ['MSFT','GME','AAPL','AMC','HOG']

for ticker in tickers:
    df = source.DataReader(ticker, data_source='yahoo', start='01-11-2021')

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


    fig = go.Figure(data=data, layout=layout)
    fig.write_html("Microsoft(MSFT) Moving Averages.html")
    fig.show()

