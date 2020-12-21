import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import datetime
import plotly
import psutil

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

time = []
cpu = []

app.layout = html.Div(children=[
    html.Div([
        html.H4('システムモニタ'),
        dcc.Graph(id='live-update-graph'),
        dcc.Interval(
            id='interval-component',
            interval=1 * 1000,  # in milliseconds
            n_intervals=0 #公式に沿って追加
        )
    ])
],)

@app.callback(Output('live-update-graph', 'figure'),
              [Input('interval-component', 'n_intervals')])
def update_graph_live(n):
    time.append(datetime.datetime.now())
    cpu.append(psutil.cpu_percent())

    fig = plotly.tools.make_subplots(rows=2, cols=1, vertical_spacing=0.2)

    fig['layout']['margin'] = {
        'l': 30, 'r': 10, 'b': 30, 't': 10
    }
    fig['layout']['legend'] = {'x': 0, 'y': 1, 'xanchor': 'left'}
    fig['layout']['yaxis1'].update(range=[0, 100])
    fig['layout']['yaxis2'].update(range=[0, 100])

    fig.append_trace({
        'x': time,
        'y': cpu,
        'name': 'cpu',
        'mode': 'lines',
        'type': 'scatter',
    }, 1, 1)

    return fig

if __name__ == '__main__':
    app.run_server(debug=False)

