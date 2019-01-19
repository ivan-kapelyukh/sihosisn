# Sells at statistically best time, within time limit
# Strategy:
#   Get a general trend using linear regressin
#   If trend is a good fit, sell accordingly
#   Otherwise, use more complex ML model

from modelling.trends import get_gradient, parse_tw_history, upward_trend

# Can use at most 29 days of transaction history from TW API
TW_MAX_MEMORY = 29


# now_date and sell_by_date should be integers
# returns whether should sell now
# rates should be sorted ascending by date, and importantly measurements should be same time apart
def should_sell(now_date, sell_by_date, rates):
    if now_date >= sell_by_date:
        return True
    interval = sell_by_date - now_date
    memory = TW_MAX_MEMORY if TW_MAX_MEMORY
    times = list(range(len(rates)))
    gradient, r2 = get_gradient(times, rates)
    print("Gradient: " + str(gradient) + ", r2: " + str(r2))
    return (not upward_trend(gradient, r2))
