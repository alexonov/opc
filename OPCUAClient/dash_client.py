import datetime

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly
from dash.dependencies import Input, Output
from opcua import Client


opc_client = Client("opc.tcp://localhost:4840/server/")
opc_client.connect()
opc_root = opc_client.get_root_node()
# parameters
temp_param = opc_root.get_child(["0:Objects", "2:Parameters", "2:Temperature"])
pres_param = opc_root.get_child(["0:Objects", "2:Parameters", "2:Pressure"])
time_param = opc_root.get_child(["0:Objects", "2:Parameters", "2:Time"])

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.layout = html.Div(
    html.Div([
        html.H4('OPC UA demo'),
        html.Div(id='live-update-text'),
        dcc.Interval(
            id='interval-component',
            interval=1*1000, # in milliseconds
            n_intervals=0
        )
    ])
)


@app.callback(Output('live-update-text', 'children'),
              [Input('interval-component', 'n_intervals')])
def update_metrics(n):
    temperature = temp_param.get_value()
    pressure = pres_param.get_value()
    time_value = time_param.get_value()

    style = {'padding': '5px', 'fontSize': '16px'}
    return [
        html.Div('Temperature: {0:.2f}'.format(temperature), style=style),
        html.Div('Pressure: {0:.2f}'.format(pressure), style=style),
        html.Div('Time: {0:0.2f}'.format(time_value), style=style)
    ]


if __name__ == '__main__':
    app.run_server(debug=True)
