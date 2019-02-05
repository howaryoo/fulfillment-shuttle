import datetime
import logging
import pytz



from dal import get_schedule

logger = logging.getLogger(__name__)


def get_time(from_, to_, when, date_param):
    schedule = get_schedule(from_, to_)
    if schedule:
        # FIXME get TZ from DB
        tz = pytz.timezone('Asia/Jerusalem')
        now = datetime.datetime.now(tz).time()
        logger.warning("current time in CGF %s", now)

        # FIXME incr time
        # delta = 5  # Minutes
        # now_plus_delta = datetime.time(now.hour, now.minute + delta)
        requested_time = None
        # TODO get from DF entities
        if when in ['next', 'now', 'soon']:
            requested_times = [time for time in schedule if time > now]
            requested_time = requested_times and requested_times[0] or None
        elif when in ['first']:
            requested_time = schedule[0]
        elif when in ['last']:
            requested_time = schedule[-1]

        if requested_time:
            return datetime.time.strftime(requested_time, '%H:%M')
