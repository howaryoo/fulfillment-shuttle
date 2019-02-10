import datetime
import logging
import pytz


from dal import get_schedule

logger = logging.getLogger(__name__)


def get_time(from_, to_, when, date_param=None, delta_amount=None, delta_unit=None):
    schedule = get_schedule(from_, to_)
    if schedule:
        # FIXME get TZ from DB
        tz = pytz.timezone('Asia/Jerusalem')
        now = datetime.datetime.now(tz)
        logger.warning("current time in CGF %s", now)
        delta = datetime.timedelta(minutes=0)
        if delta_amount and delta_unit:
            if delta_unit.startswith('m'):
                delta = datetime.timedelta(minutes=delta_amount)
            elif delta_unit.startswith('h'):
                delta = datetime.timedelta(hours=delta_amount)

        now_plus_delta = now + delta
        requested_time = None
        # TODO get from DF entities
        if when in ['next', 'now', 'soon']:
            requested_times = [time for time in schedule if time > now_plus_delta.time()]
            requested_time = requested_times and requested_times[0] or None
        elif when in ['first']:
            requested_time = schedule[0]
        elif when in ['last']:
            requested_time = schedule[-1]

        if requested_time:
            return datetime.time.strftime(requested_time, '%H:%M')
