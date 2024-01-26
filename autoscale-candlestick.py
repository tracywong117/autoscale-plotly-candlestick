import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import pandas as pd

from dash.exceptions import PreventUpdate

df = pd.read_csv("finance-charts-apple.csv")
df.columns = [col.replace("AAPL.", "") for col in df.columns]

stockfig = go.Figure(
    {
        "data": [
            {
                "type": "candlestick",
                "x": df["Date"],
                "open": df["Open"],
                "high": df["High"],
                "low": df["Low"],
                "close": df["Close"],
                "xaxis": "x",
                "yaxis": "y",
            }
        ],
        "layout": {
            "height": 700,
            "title": "AAPL Stock Price",
            "xaxis": {"type": "date", "rangeslider": {"yaxis": {"rangemode": "auto"}}},
        },
    }
)

app = dash.Dash(__name__)

app.layout = html.Div(
    [
        dcc.Graph(id="stock-chart", figure=stockfig, style={"width": "1300px"}),
        html.Div(id="range-output"),
    ]
)


def find_min_max(df, start_date, end_date):
    df["Date"] = pd.to_datetime(df["Date"])
    filtered_df = df[(df["Date"] >= start_date) & (df["Date"] <= end_date)]
    # print(filtered_df)
    min_values = min(list(filtered_df[["Open", "High", "Low", "Close"]].min()))
    max_values = max(list(filtered_df[["Open", "High", "Low", "Close"]].max()))
    # print(min_values, max_values)
    return min_values, max_values


@app.callback(Output("stock-chart", "figure"), [Input("stock-chart", "relayoutData")])
def display_relayout_data(relayoutData):
    global stockfig
    start = end = 0

    if not relayoutData:
        raise PreventUpdate

    if relayoutData.get("xaxis.range", False):
        start = relayoutData["xaxis.range"][0]
        end = relayoutData["xaxis.range"][1]
    elif relayoutData.get("xaxis.range[0]", False):
        start = relayoutData["xaxis.range[0]"]
        end = relayoutData["xaxis.range[1]"]

    if start != 0:
        print("Start: ", start.split(" ")[0])
        print("End: ", end.split(" ")[0])
        start = start.split(" ")[0]
        end = end.split(" ")[0]

        ymin, ymax = find_min_max(df, start, end)

        diff = ymax - ymin

        ymin -= min(diff * 0.2, 2)
        ymax += min(diff * 0.2, 2)

        stockfig.update_layout(
            xaxis_autorange=False,
            yaxis_autorange=False,
            xaxis_range=[start, end],
            yaxis_range=[ymin, ymax],
        )

        return stockfig
    else:
        raise PreventUpdate


# Run the app
if __name__ == "__main__":
    app.run_server(debug=True, port=8051)
