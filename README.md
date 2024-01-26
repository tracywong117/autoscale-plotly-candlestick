## Autoscale y-axis of candlestick when using rangeslider

When using Plotly Python to plot candlestick charts for stock prices, one may encounter the issue that the y-axis does not autoscale when using the rangeslider to select a specific range of data. This code snippet provides a solution by utilizing a Dash callback for relayout, which allows for obtaining the range selected by the user and adjust the y-axis accordingly.

![Demo](Demo.png)