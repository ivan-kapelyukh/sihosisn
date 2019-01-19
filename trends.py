import matplotlib.pyplot as plt
from scipy import stats

# returns [gradient, certainty], where certainty is goodness of fit in terms of r-squared value
def getGradient(times, rates):
    gradient, intercept, r_value, p_value, std_err = stats.linregress(
        times, rates)
    r2 = r_value**2
    print("gradient: %f    r2: %f" % (gradient, r2))
    return [gradient, r2]