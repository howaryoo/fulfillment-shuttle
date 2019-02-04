import datetime

from google.cloud import firestore

db = firestore.Client()

schedule_ref = db.collection(u'schedule')


def get_schedule(from_, to_):
    query_ref = schedule_ref.where(u'from', u'==', from_).where(u'to', u'==', to_)
    doc = next(query_ref.get())
    schedule = doc.to_dict()
    schedule_time = [datetime.time(int(hour), int(minute)) for hour, minute in
                     [timestr.split(':') for timestr in schedule['times']]]
    schedule_time.sort()
    return schedule_time
