
def get_future_value_of_annuity(monthly_contribution, annual_rate_of_return, years, compounding_frequency):

    future_value = monthly_contribution * \
                   (((1 + annual_rate_of_return/compounding_frequency) ** (compounding_frequency * years)) - 1) / \
                   (annual_rate_of_return / compounding_frequency)

    return future_value
