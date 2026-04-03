import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
from tinydb import TinyDB

db = TinyDB('/home/doniczka/app/db.json')
app = dash.Dash(__name__)

app.layout = html.Div(style={'fontFamily': 'sans-serif', 'textAlign': 'center', 'color': 'white', 'backgroundColor': '#0e1117', 'minHeight': '100vh', 'paddingTop': '50px'}, children=[
    html.H1("Status Nawodnienia"),
    html.Div(id='live-update-text', style={'fontSize': '60px', 'fontWeight': 'bold', 'margin': '20px'}),
    html.Div(id='live-update-status', style={'fontSize': '24px', 'fontWeight': 'bold', 'padding': '15px', 'display': 'inline-block', 'borderRadius': '5px'}),
    dcc.Graph(id='live-update-graph'),
    dcc.Interval(id='interval-component', interval=60*1000, n_intervals=0)
])

@app.callback(
    [Output('live-update-text', 'children'),
     Output('live-update-status', 'children'),
     Output('live-update-status', 'style'),
     Output('live-update-graph', 'figure')],
    [Input('interval-component', 'n_intervals')]
)
def update_metrics(n):
    records = db.all()
    if not records:
        return "Brak danych", "", {'display': 'none'}, {}

    df = pd.DataFrame(records)
    df['time'] = pd.to_datetime(df['time'])
    df = df.sort_values('time')
    current = df.iloc[-1]['moisture']

    status_text = "Gleba nawodniona." if current >= 30.0 else "Wymagane podlanie."
    bg_color = "#09ab3b" if current >= 30.0 else "#ff2b2b"
    status_style = {'fontSize': '24px', 'fontWeight': 'bold', 'padding': '15px', 'display': 'inline-block', 'borderRadius': '5px', 'backgroundColor': bg_color, 'color': 'white'}

    fig = {
        'data': [{'x': df['time'], 'y': df['moisture'], 'type': 'scatter', 'mode': 'lines', 'line': {'color': '#00a4d6'}}],
        'layout': {
            'plot_bgcolor': '#0e1117', 
            'paper_bgcolor': '#0e1117', 
            'font': {'color': 'white'},
            'margin': {'l': 40, 'r': 40, 't': 40, 'b': 40}
        }
    }

    return f"{current}%", status_text, status_style, fig

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8501, debug=False)
