def format_seconds(seconds):
    """Format seconds as Hours:Minutes:seconds"""
    total_seconds = int(seconds)
    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return "{:02}:{:02}:{:02}".format(hours, minutes, seconds)


def compute_eta(time_per_step, remaining_steps, previous_eta=None, beta=0.95):
    """Estimated Time of Arrival with exponential moving average.
    Beta is the exponential decay factor,
    i.e. the weight given to the previous eta."""
    raw_eta = remaining_steps*time_per_step
    if previous_eta is None:
        return raw_eta
    return raw_eta*(1-beta) + previous_eta*beta
