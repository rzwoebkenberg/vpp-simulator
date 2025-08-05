from dash import Dash, html, dcc, Input, Output, callback
import plotly.express as px
import pandas as pd

app = Dash()

df = pd.read_csv('../bin/history.csv')
ders_list = df.der_name.unique()

app.layout = html.Div([
    html.H1(children='VPP Sim Snapshot', style={'textAlign': 'center'}),
    dcc.Dropdown([{'label': name, 'value': name} for name in df.der_name.unique()], ders_list[0], id='ders-dropdown'),
    dcc.Graph(id='graph-content')
])

@callback(
    Output('graph-content', 'figure'),
    Input('ders-dropdown', 'value')
)

def update_output(value):
    dff = df[df.der_name==value]
    if 'Battery' in value:
        return px.line(dff, x='time_hr', y='soc_percent')
    elif 'Solar' in value:
        return px.line(dff, x='time_hr', y='actual_power_kw')
    else:
        return px.line()

if __name__ == '__main__':
    app.run(debug=True)
