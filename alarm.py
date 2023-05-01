import time
import uuid

import alertness_detection as ad

ALARMS = []


def get_alarms():
    return ALARMS


def create(new_alarm):
    ALARMS.append({
        "id": uuid.uuid4().hex,
        "hour": new_alarm[0],
        "min": new_alarm[1],
        "status": "active"
    })
    return


def delete(alarm_id):
    for a in ALARMS:
        if a["id"] == alarm_id:
            ALARMS.remove(a)
            return True
    return False


def try_ring():
    curr_time = time.localtime()
    ring_alarm = False
    for a in ALARMS:
        if a["hour"] == curr_time.tm_hour \
                and a["min"] == curr_time.tm_hour \
                and a["status"] == "active":
            a["status"] = "ringing"
            ring_alarm = True
    if ring_alarm:
        ad.trigger_alarm()
    return


def silence():
    ad.silence_alarm()
    for a in ALARMS:
        if a["status"] == "ringing":
            a["status"] = "disabled"
    return


def snooze():
    ad.silence_alarm()
    curr_time = time.localtime()
    minute = curr_time.tm_min + 5
    hour = curr_time.tm_hour
    if minute >= 60:
        hour += 1
        minute = minute % 60
        if hour >= 24:
            hour = hour % 24
    create((hour, minute))
    return
