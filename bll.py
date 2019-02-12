import datetime
import logging
import pytz


from dal import get_schedule

logger = logging.getLogger(__name__)


def get_time(from_, to_, when, date_param=None, delta_amount=None, delta_unit=None, returned_time=None):
    """

    :param from_: string, for now "atidim", "universita"
    :param to_: same
    :param when: "soon", "first", "last"
    :param date_param:  time, string, 24 hr clock 16:04 semi military time
    :param delta_amount:
    :param delta_unit:
    :param returned_time:
    :return:
    """
    schedule = get_schedule(from_, to_)
    if schedule:
        # FIXME get TZ from DB
        tz = pytz.timezone('Asia/Jerusalem')
        now = datetime.datetime.now(tz)
        if returned_time:
            hour, min = map(int, returned_time.split(':'))
            now = now.replace(hour=hour, minute=min)
        logger.warning("current time in CGF %s", now)
        delta = datetime.timedelta(minutes=0)
        if delta_amount and delta_unit:
            if delta_unit.startswith('m'):
                delta = datetime.timedelta(minutes=delta_amount)
            elif delta_unit.startswith('h'):
                delta = datetime.timedelta(hours=delta_amount)

        now_plus_delta = now + delta
        print(f"now_plus_delta: {now_plus_delta}")
        requested_time = None
        # TODO get from DF entities
        if when in ['next', 'now', 'soon', 'after']:
            requested_times = [time for time in schedule if time > now_plus_delta.time()]
            requested_time = requested_times and requested_times[0] or None
        elif when in ['first']:
            requested_time = schedule[0]
        elif when in ['last']:
            requested_time = schedule[-1]

        if requested_time:
            return datetime.time.strftime(requested_time, '%H:%M')

def datetime_time_to_timedeltha(t):
    import datetime
    return datetime.timedelta(hours=t.hour, minutes=t.minute, seconds=t.second)

def two_datetime_time_to_second_dif(t, t1):
    d, d1 = datetime_time_to_timedeltha(t), datetime_time_to_timedeltha(t1)
    return abs(d.total_seconds() - d1.total_seconds())

def str2datatime_time(s):
    import datetime
    h, m = map(lambda x: int(x), s.split(":"))
    return datetime.time(hour=h, minute=m)

def get_closest_times(s, from_, to_):
    """

    :param s: time string in 24 hr format hh:mm
    :return: 3 closest times.
    """
    data = get_schedule(from_, to_)
    time_dist = map(lambda x: two_datetime_time_to_second_dif(str2datatime_time(s), x), data)
    values = sorted(zip(time_dist, data), key=lambda x: x[0])
    return list(map(lambda x:x[1], values))


import time
import datetime
data = get_schedule("atidim", "universita")
data1, data2 = data[0], data[1]
print(two_datetime_time_to_second_dif(data1, data2))
m = get_closest_times("12:34", "atidim", "universita")
print(m)