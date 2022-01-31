import uuid
import datetime
import calendar

def get_utc_timestamp():
    current_datetime = datetime.datetime.utcnow()
    current_timetuple = current_datetime.utctimetuple()
    current_timestamp = calendar.timegm(current_timetuple)
    return current_timestamp

def get_unique_id():
    return uuid.uuid4().hex

def generate_unique_string():
    timestamp=get_utc_timestamp()
    uniqueid=get_unique_id()
    return str(timestamp)+"_"+str(uniqueid)
