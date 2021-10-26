from jupyter_dash import JupyterDash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd


def get_pandas_col_dataset(df: pd.DataFrame, width: int = 40):
    app = JupyterDash(__name__)
    app.layout = html.Div([
        html.Div([
            html.Div([
                dcc.Dropdown(
                    id='column',
                    options=[{'label': i, 'value': i} for i in df],
                    value='a_mean',
                )
            ], style={'width': f'{width}%', 'display': 'inline-block'}),

            html.Div([
                dcc.Graph(id='indicator-graphic')], style={'width': f'{width + 8}%'})
        ])])

    @app.callback(
        Output('indicator-graphic', 'figure'),
        Input('column', 'value'))
    def update_graph(column,
                     radio_dataset):
        fig = px.scatter(x=range(len(df)),
                         y=df[column], template='plotly_white')

        fig.update_layout(template='plotly_white')
        return fig

    return app
