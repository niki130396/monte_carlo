import dash
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template
from dash.dependencies import Input, Output
import plotly.express as px
import numpy as np
from scipy.stats import t

from redis import Redis

from utils.future_value import get_future_value_of_annuity
from definitions import (
    S_AND_P_MEAN_RETURNS,
    S_AND_P_STANDARD_DEVIATION,
    AAPL_MEAN_RETURNS,
    AAPL_STANDARD_DEVIATION,
)


load_figure_template("LUX")

r = Redis(host='localhost', port=6379, decode_responses=True)

for ticker, mean_return, standard_deviation in [
    ("s_and_p", S_AND_P_MEAN_RETURNS, S_AND_P_STANDARD_DEVIATION),
    ("aapl", AAPL_MEAN_RETURNS, AAPL_STANDARD_DEVIATION)
]:
    random_numbers = np.random.standard_t(5, size=10000)
    scaled_and_shifted_t = (random_numbers * standard_deviation) + mean_return
    x = np.linspace(mean_return - 3 * standard_deviation,
                    mean_return + 3 * standard_deviation, 10000)
    pdf = t.pdf((x - mean_return) / standard_deviation, 5).tolist()

    r.rpush(ticker, *pdf)

SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "24rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}


sidebar = html.Div(
    [
        html.H2("Filters"),
        html.Hr(),
        html.P(
            "A simple sidebar layout with filters", className="lead"
        ),
        dbc.Nav(
            [
                dcc.Dropdown(
                    id="ticker_choice",
                    options=[
                        {'label': 'S&P 500', 'value': 's_and_p'},
                        {'label': 'AAPL', 'value': 'aapl'},
                    ],
                    style={'width': '50%'}
                ),
                html.Br(),
                dcc.Input(
                    id='monthly_contribution',
                    type='number',
                    placeholder='Monthly contribution (the amount you will invest every month)',
                    value=1000,
                    style={'width': '50%'}
                ),
                html.Br(),
                dcc.Input(
                    id='total_period',
                    type='number',
                    placeholder='The total period of the observation (how many years you are planning to invest)',
                    value=10,
                    style={'width': '50%'}
                ),
                html.Br(),
                dcc.Input(
                    id='compounding_frequency',
                    type='number',
                    placeholder='The amount of compounding per period (e.g. monthly compounding, daily compounding...)',
                    value=12,
                    style={'width': '50%'}
                )

            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)

app = dash.Dash(external_stylesheets=[dbc.themes.LUX])

app.layout = html.Div(children=[
                dbc.Row([
                    dbc.Col(),
                    dbc.Col(
                        html.H1('Welcome to my dash app'),
                        width=9,
                        style={'margin-left': '7px', 'margin-top': '7px'}
                    )
                ]),
                dbc.Row([
                    dbc.Col(sidebar),
                    dbc.Col(
                        dcc.Graph(id='distribution_plot'),
                        width=9,
                        style={'margin-left': '15px', 'margin-top': '7px', 'margin-right': '15px'})
                ])
    ]
)


# Define callback to update the plot based on user input
@app.callback(
    Output('distribution_plot', 'figure'),
    [
        Input('monthly_contribution', 'value'),
        Input('total_period', 'value'),
        Input('compounding_frequency', 'value'),
        Input('ticker_choice', 'value'),
    ]
)
def update_distribution_plot(monthly_contribution, total_period, compounding_frequency, ticker_choice):

    random_returns = [float(value) for value in r.lrange(ticker_choice, 0, -1)]

    future_values = [
        get_future_value_of_annuity(
            monthly_contribution,
            random_return,
            total_period,
            compounding_frequency
        ) / 1000
        for random_return in random_returns
    ]

    print(future_values[0])
    # Generate histogram
    fig = px.histogram(future_values, nbins=25, title='Distribution Plot of Future Value of Investments in S&P 500 Index',
                       labels={'value': 'Future Value (in thousands of dollars)', 'count': 'Frequency (Density)'})

    return fig


# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
