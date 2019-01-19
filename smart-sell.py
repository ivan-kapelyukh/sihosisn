from trends import get_gradient, parse_tw_history, upward_trend


# now_date and sell_by_date should be integers
def smart_sell(now_date, sell_by_date, profile, recipient, amount):
    INIT_MEMORY = 29
    memory = INIT_MEMORY

    # TODO: fetch this from API call instead
    f = open("./tw-history", "r")
    times, rates = parse_tw_history(f.read())
    normalised_times = list(range(NUM_POINTS))

    return 1
