import time
import alertness_detection as ad
import voice_commands as vc
from pygame import mixer
from threading import Thread, Event
import uuid
from enum import Enum
from middleware import increase_time_by, convert_str_to_t_tup
from events import get_soonest_event, Importance

Status = Enum('Status', ['ACTIVE', 'RINGING', 'DISABLED'])
Mode = Enum('Mode', ['BASIC', 'QUE_SERA_SERA', 'AT_ALL_COSTS'])

event = Event()
ALARMS = []
mixer.init()
alarm = mixer.music
alarm.load('mixkit-sleepy-cat-135.mp3')


def get_alarms():
    return ALARMS.copy()


def create(new_alarm, mode):
    ALARMS.append({
        "id": uuid.uuid4().hex,
        "hour": int(new_alarm[0]),
        "min": int(new_alarm[1]),
        "status": Status.ACTIVE.name,
        "mode": mode
    })
    return


def delete(alarm_id):
    for a in ALARMS:
        if a["id"] == alarm_id:
            ALARMS.remove(a)
            return True
    return False


def silence():
    alarm.stop()
    event.set()
    for a in ALARMS:
        if a["status"] == Status.RINGING.name:
            a["status"] = Status.DISABLED.name
    return


def try_ring():
    curr_time = time.localtime()
    ring_alarm = False
    for a in ALARMS:
        if a["hour"] == curr_time.tm_hour \
                and a["min"] == curr_time.tm_min \
                and a["status"] == Status.ACTIVE.name:
            a["status"] = Status.RINGING.name
            ring_alarm = True
    if ring_alarm:
        event.clear()
        camera_detection = Thread(target=ad.trigger_alarm, args=(event,))
        vocal_command = Thread(target=vc.get_voice_command, args=(event,))
        alarm.play(loops=-1)
        camera_detection.start()
        vocal_command.start()
        event.wait()
        alarm.stop()
        camera_detection.join()
        vocal_command.join()
    return


def snooze():
    silence()
    curr_time = time.localtime()
    create(increase_time_by((curr_time.tm_hour, curr_time.tm_min)))
    return


def schedule_next_alarm():
    soonest_event = get_soonest_event()
    if soonest_event:
        event_time = convert_str_to_t_tup(soonest_event)
        if soonest_event['importance'] == Importance.HIGH.name:
            create(event_time, Mode.AT_ALL_COSTS.name)
        elif soonest_event['importance'] == Importance.MED.name:
            create(event_time, Mode.BASIC.name)
        else:
            create(event_time, Mode.QUE_SERA_SERA)
    return


if __name__ == '__main__':
    try_ring()
    print("done")
