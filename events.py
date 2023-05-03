from enum import Enum
import uuid
import datetime
from middleware import is_after, convert_str_to_t_tup

Importance = Enum('Importance', ['HIGH', 'MEDIUM', 'LOW', 'ZERO'])

EVENTS = {}


def get_date_key(date):
    date_info = date.split(":")
    return datetime.datetime(*date_info)


def get_all_events():
    return EVENTS.copy()


def get_events_from(start_date, end_date):
    mini_calendar = []
    current_key = get_date_key(start_date)
    end_key = get_date_key(end_date)
    while current_key <= end_key:
        event_data = {
            'date': str(current_key.month) + "/" + str(current_key.day),
            'weekday': current_key.isoweekday()
        }
        if current_key in EVENTS.keys():
            event_data.update(EVENTS[current_key])
        mini_calendar.append(event_data)
        current_key += datetime.timedelta(days=1)
    return mini_calendar


def create(date, name, importance, t_start, t_end):
    date_key = get_date_key(date)
    event_data = {
        "id": uuid.uuid4().hex,
        'name': name,
        'importance': importance,
        'start_time': t_start,
        'end_time': t_end
    }
    if date_key in EVENTS.keys():
        EVENTS[date_key].append(event_data)
    else:
        EVENTS[date_key] = event_data
    return


def delete(date, event_id):
    date_key = get_date_key(date)
    for e in EVENTS[date_key]:
        if e['id'] == event_id:
            EVENTS[date_key].remove(e)
            return True
    return False


def get_soonest_event():
    curr_date_key = datetime.datetime.now()
    curr_time = (curr_date_key.hour, curr_date_key.minute)
    soonest_event = None
    soonest_time = None
    if curr_date_key in EVENTS.keys():
        for e in EVENTS[curr_date_key]:
            event_time = convert_str_to_t_tup(e.start_time)
            if is_after(event_time, curr_time) and \
                    (not soonest_event or is_after(soonest_time, event_time)):
                soonest_time = event_time
                soonest_event = e
    if not soonest_event:
        next_date_key = curr_date_key + datetime.timedelta(days=1)
        if next_date_key in EVENTS.keys():
            event_time = convert_str_to_t_tup(e.start_time)
            for e in EVENTS[next_date_key]:
                if not soonest_event or is_after(soonest_time, event_time):
                    soonest_time = event_time
                    soonest_event = e
    return soonest_event

