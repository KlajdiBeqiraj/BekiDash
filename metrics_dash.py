import matplotlib.pyplot as plt
import pandas as pd
from jupyter_dash import JupyterDash
import plotly.express as px
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output


# function used to plot two confusion matrix with a subplot
def confusion_matrix_subplot(cm_1, cm_2):
    fig, ax = plt.subplots(1, 2, figsize=(10, 10))
    ax[0].set_xticklabels(['', 'baseline', 'stress'])
    ax[0].set_yticklabels(['', 'baseline', 'stress'])
    ax[1].set_xticklabels(['', 'baseline', 'stress'])
    ax[1].set_yticklabels(['', 'baseline', 'stress'])

    conf_matrix = cm_1
    ax[0].matshow(conf_matrix, cmap=plt.cm.Blues, alpha=0.3)
    for i in range(conf_matrix.shape[0]):
        for j in range(conf_matrix.shape[1]):
            ax[0].text(x=j, y=i, s=conf_matrix[i, j], va='center', ha='center', size='xx-large')
    ax[0].set_title('Confusion Matrix: Training', fontsize=15)

    conf_matrix = cm_2
    ax[1].matshow(conf_matrix, cmap=plt.cm.Blues, alpha=0.3)
    for i in range(conf_matrix.shape[0]):
        for j in range(conf_matrix.shape[1]):
            ax[1].text(x=j, y=i, s=conf_matrix[i, j], va='center', ha='center', size='xx-large')
    ax[1].set_title('Confusion Matrix: Test', fontsize=15)

    plt.show()


# function used to plot all metrics with a dash
def get_metrics_dash(metrics: dict, width: int = 40):
    app = JupyterDash(__name__)

    options = []
    for key in metrics:
        tmp = {}
        if 'val' not in key:
            tmp['label'] = key
            tmp['value'] = key
            options.append(tmp)

    app.layout = html.Div([
        html.Div([
            html.Div([
                dcc.Dropdown(
                    id='column',
                    options=options,
                    value='loss',
                )
            ], style={'width': f'{width}%', 'display': 'inline-block', }),

            html.Div([
                dcc.Graph(id='indicator-graphic')], style={'width': f'{width}%'})
        ])])

    @app.callback(
        Output('indicator-graphic', 'figure'),
        Input('column', 'value'))
    def update_graph(column):
        df = pd.DataFrame.from_dict(metrics)
        fig = px.line(df, x=range(len(df)),
                      y=[f'{column}', f'val_{column}'], template='plotly_white')
        fig.update_layout(margin={'l': 40, 'b': 40, 't': 10, 'r': 0}, hovermode='closest')
        return fig

    return app


def get_metrics_plots(metrics):
    df = pd.DataFrame.from_dict(metrics)

    for column in df.columns:
        if 'val' not in column:
            fig = px.line(df, x=range(len(df)),
                          y=[f'{column}', f'val_{column}'], template='plotly_white')
            fig.update_layout(height=280, width=800, title_text=f"{column}", title_x=0.5)
            fig.show()
