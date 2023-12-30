import numpy as np
from scipy.stats import t
import plotly.express as px
import matplotlib.pyplot as plt

from definitions import (
    S_AND_P_MEAN_RETURNS,
    S_AND_P_STANDARD_DEVIATION,
    AAPL_MEAN_RETURNS,
    AAPL_STANDARD_DEVIATION,
)
from utils.future_value import get_future_value_of_annuity

random_numbers = np.random.standard_t(5, size=10000)
scaled_and_shifted_t = (random_numbers * AAPL_STANDARD_DEVIATION) + AAPL_MEAN_RETURNS
x = np.linspace(AAPL_MEAN_RETURNS - 3 * AAPL_STANDARD_DEVIATION,
                AAPL_MEAN_RETURNS + 3 * AAPL_STANDARD_DEVIATION, 10000)
pdf = t.pdf((x - AAPL_MEAN_RETURNS) / AAPL_STANDARD_DEVIATION, 5).tolist()

print(scaled_and_shifted_t)
print(x)
print(pdf)


future_values = [
    get_future_value_of_annuity(
        4000,
        random_return,
        10,
        12
    ) / 1000
    for random_return in pdf
]


fig = px.histogram(future_values, nbins=50, title='Distribution Plot of Future Value of Investments in S&P 500 Index',
                   labels={'value': 'Future Value (in thousands of dollars)', 'count': 'Frequency (Density)'})

fig.show()


# # Generate random numbers from a t-distribution
# df = 5  # degrees of freedom
# random_returns = np.random.standard_t(df, size=10000)
#
# scaled_and_shifted_t = (random_returns * S_AND_P_STANDARD_DEVIATION) + S_AND_P_MEAN_RETURNS
# # Create a histogram using Plotly Express
# fig = px.histogram(x=scaled_and_shifted_t, nbins=30, histnorm='probability density', marginal='rug',
#                    title='Histogram with PDF Overlay', labels={'x': 'Random Returns'})
#
# # Overlay theoretical PDF
# x_values = np.linspace(min(scaled_and_shifted_t), max(scaled_and_shifted_t), 10000)
# pdf_values = t.pdf(x_values, df)
# fig.add_scatter(x=x_values, y=pdf_values, mode='lines', name='PDF', line=dict(color='red', width=2))
#
# # Show the plot
# fig.show()

# future_values = [
#     get_future_value_of_annuity(
#         4000,
#         random_return,
#         10,
#         12
#     ) / 1000
#     for random_return in pdf_values
# ]
#
# fig = px.histogram(future_values, nbins=25, title='Distribution Plot of Future Value of Investments in S&P 500 Index',
#                    labels={'value': 'Future Value (in thousands of dollars)', 'count': 'Frequency (Density)'})
#
# fig.show()
