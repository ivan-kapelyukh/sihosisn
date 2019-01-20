# Sells at statistically best time, within time limit
# Strategy:
#   Get a general trend using linear regressin
#   If trend is a good fit, sell accordingly
#   Otherwise, use more complex ML model

from modelling.trends import get_gradient, parse_tw_history, upward_trend
from math import exp

# Can use at most 29 days of transaction history from TW API
TW_MAX_MEMORY = 29


# now_date and sell_by_date should be integers
# returns whether should sell now
# rates should be sorted ascending by date, and importantly measurements should be same time apart
def should_sell(now_date, sell_by_date, rates):
    if now_date >= sell_by_date:
        return True
    interval = sell_by_date - now_date
    times = list(range(len(rates)))
    gradient, r2 = get_gradient(times, rates)
    print("Gradient: " + str(gradient) + ", r2: " + str(r2))
    return (not upward_trend(gradient, r2))


# returns value between 0.0 and 1.0 inclusive
# rates should be sorted ascending by date, ending in latest reading, and importantly measurements should be same time apart
# fraction is of what you have left now, not of what you started with
# number of transfers should be a function of user-inputted "risk"
# function should be called more frequently for more transfers
def fraction_to_sell(original_date, now_date, sell_by_date, rates,
                     num_transfers):
    if now_date >= sell_by_date:
        return 1.0

    fraction = 1.0

    full_interval = sell_by_date - original_date
    interval_left = sell_by_date - now_date
    memory = min(full_interval, len(rates),
                 TW_MAX_MEMORY)  # TODO: pick optimally
    print("Mem: " + str(memory))
    times = list(range(memory))
    rates = rates[-memory:]
    gradient, r2 = get_gradient(times, rates)
    # decreases as gradient increases
    gradient_factor = exp(-1.0 * gradient)
    trend_factor = gradient_factor
    # * (r2 / 0.5)
    # TODO: re-add
    # ooh, low r2 probs means we're at a peak/trough?

    dca_factor = 1.0 / num_transfers

    motivation_factor = 1.0 / interval_left

    print("DCA: " + str(dca_factor) + ", trend: " + str(trend_factor) +
          ", motivation: " + str(motivation_factor))
    fraction *= dca_factor * trend_factor
    # * motivation_factor
    # TODO: re-add

    return min(1.0, fraction)


print("POSITIVE TREND TEST:")
hist = [2, 3, 3, 4, 7]
future = [8, 10, 12, 14, 16]
for day in range(5):
    print("For day = " + str(day) + ", selling fraction: " +
          str(fraction_to_sell(0, day, 4, hist, 5)))
    hist.pop(0)
    hist.append(future.pop(0))
print("-----")

print("NEGATIVE TEST:")
hist = [10, 9, 8, 6, 6]
future = [5, 4, 4, 4, 4]
for day in range(5):
    print("For day = " + str(day) + ", selling fraction: " +
          str(fraction_to_sell(0, day, 4, hist, 5)))
    hist.pop(0)
    hist.append(future.pop(0))
print("-----")

print("PEAK TEST:")
hist = [1, 1, 1, 2, 2, 2, 4, 4, 6, 7, 10]
future = [12, 10, 10, 8, 4, 1, 1]
for day in range(5):
    print("For day = " + str(day) + ", selling fraction: " +
          str(fraction_to_sell(0, day, 4, hist, 5)))
    hist.pop(0)
    hist.append(future.pop(0))
print("-----")

print("SLIGHT NEGATIVE TEST:")
hist = [1.030, 1.026, 1.025, 1.019, 1.018]
future = [1.018, 1.015, 1.011, 1.009, 1.008]
for day in range(5):
    print("For day = " + str(day) + ", selling fraction: " +
          str(fraction_to_sell(0, day, 4, hist, 5)))
    hist.pop(0)
    hist.append(future.pop(0))
print("-----")

print("SLIGHT POSITIVE TEST:")
hist = [1002, 1005, 1006]
future = [1007, 1008, 1009, 1009, 1015]
for day in range(5):
    print("For day = " + str(day) + ", selling fraction: " +
          str(fraction_to_sell(0, day, 4, hist, 5)))
    hist.pop(0)
    hist.append(future.pop(0))
print("-----")

print("SLIGHT POSITIVE TEST WITH TWIST:")
hist = [1002, 1005, 1006]
future = [1007, 1008, 750, 560, 240]
for day in range(5):
    print("For day = " + str(day) + ", selling fraction: " +
          str(fraction_to_sell(0, day, 5, hist, 5)))
    hist.pop(0)
    hist.append(future.pop(0))
print("-----")
