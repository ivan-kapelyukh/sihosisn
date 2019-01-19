import matplotlib.pyplot as plt
import json
from scipy import stats


# returns [gradient, certainty], where certainty is goodness of fit in terms of r-squared value
# note that times should be integers, e.g. 1 for Day 1, 2 for Day 2
def get_gradient(times, rates):
    gradient, intercept, r_value, p_value, std_err = stats.linregress(
        times, rates)
    r2 = r_value**2
    print("gradient: %f    r2: %f" % (gradient, r2))
    return [gradient, r2]


# takes string in JSON format, i.e. array of JSON objects
# returned in time-wise ascending order (oldest first)
def parse_tw_history(history):
    readings = json.loads(history)
    times = []
    rates = []
    for reading in readings:
        times.append(reading['time'])
        rates.append(reading['rate'])
    times.reverse()
    rates.reverse()
    return [times, rates]


# passes if rate is increasing, and we are quite sure of this
def upward_trend(gradient, certainty):
    MIN_GRAD = 0.0
    MIN_CERTAINTY = 0.5
    if (gradient > MIN_GRAD and certainty > MIN_CERTAINTY):
        return "hold"
    else:
        return "sell"
