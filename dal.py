import datetime
import logging

logger = logging.getLogger(__name__)

try:
    import firebase_admin
    from firebase_admin import firestore

    cred = firebase_admin.credentials.Certificate(
        "/home/arye/Downloads/fuseteam3-firebase-adminsdk-z6q2n-462e35b9a1.json")
    firebase_admin.initialize_app(cred)
    db = firebase_admin.firestore.client()
except:
    from google.cloud import firestore
    db = firestore.Client()

schedule_ref = db.collection(u'schedule')


def get_schedule(from_, to_):
    query_ref = schedule_ref.where(u'from', u'==', from_).where(u'to', u'==', to_)
    try:
        doc = next(query_ref.get())
    except StopIteration:
        logger.warning("No schedule from %s to %s", from_, to_)
    else:
        schedule = doc.to_dict()
        schedule_time = [datetime.time(int(hour), int(minute)) for hour, minute in
                         [timestr.split(':') for timestr in schedule['times']]]
        schedule_time.sort()
        return schedule_time
