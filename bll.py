import datetime

from dal import get_schedule


def get_time(from_, to_, when, date_param):
    schedule = get_schedule(from_, to_)
    now = datetime.datetime.now().time()
    delta = datetime.timedelta(minutes=5)
    requested_time = None
    # TODO get from entities
    if when in ['next', 'now', 'soon']:
        requested_times = [time for time in schedule if time > now + delta]
        requested_time = requested_times and requested_times[0] or None
    elif when in ['first']:
        requested_time = schedule[0]
    elif when in ['last']:
        requested_time = schedule[-1]

    if requested_time:
        return datetime.time.strftime(requested_time, '%H:%M')
