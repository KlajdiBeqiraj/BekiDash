from jupyter_dash import JupyterDash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import numpy as np


# dash che data un numpy array fa il plot di n seq scelte dallo slider e di permette di decidere quale colona vuoi plottare
def get_sequences_dash(x_train: np.ndarray,
                       y_train: np.ndarray,
                       col_name: list,
                       width: int = 30):
    options = []
    for i in range(len(col_name)):
        dic = {
                'label': col_name[i],
                'value': i
              }
        options.append(dic)

    app = JupyterDash(__name__)

    app.layout = html.Div([
        html.Div([
            html.Div([
                html.Div([
                    html.H5(f"Starting index (max value = {x_train.shape[0] - 10}):"),
                ], style={'width': f'{width + 10}%', 'display': 'inline-block'}),

                html.Div([
                    dcc.Input(
                        id='starting_index',
                        type='number',
                        value=100
                    ),

                ], style={'width': f'{width}%', 'display': 'inline-block'}),

            ], style={'width': f'{width + 15}%'}),
            html.Div([
                dcc.Dropdown(
                    id='column',
                    options=options,
                    value=0,
                ),

            ], style={'width': f'{width + 10}%', 'display': 'inline-block'}),

            html.Div([
                dcc.Graph(id='indicator-graphic')], style={'width': f'{width + 18}%'}),

            html.Div([
                html.Div([
                    html.H5("N° sequences:"),
                ], style={'width': '20%'}),
                html.Div([
                    dcc.Slider(
                        id='num_seq_slider',
                        min=1,
                        max=10,
                        value=4,
                        marks={i: str(i) for i in range(1, 11)},
                        step=None
                    )], style={'width': '100%'})

            ], style={'width': f'{width + 10}%', 'display': 'inline-block'})
        ])])

    @app.callback(
        Output('indicator-graphic', 'figure'),
        Input('column', 'value'),
        Input('starting_index', 'value'),
        Input('num_seq_slider', 'value'),
    )
    def update_graph(column, starting_index, num_seq_slider):

        fig = go.Figure()

        for i in range(starting_index, starting_index + num_seq_slider):
            if y_train[i] == 1:
                fig.add_trace(go.Scatter(x=np.arange(x_train[i, :, column].shape[0]), y=x_train[i, :, column],
                                         marker=dict(color='red'), name=f'Seq {i}: stress'))
            else:
                fig.add_trace(go.Scatter(x=np.arange(x_train[i, :, column].shape[0]), y=x_train[i, :, column],
                                         marker=dict(color='blue'), name=f'Seq {i}: baseline'))

        fig.update_layout(margin={'l': 40, 'b': 40, 't': 10, 'r': 0}, hovermode='closest', template='plotly_white')

        return fig

    return app
