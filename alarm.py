import time
import alertness_detection as ad
import voice_commands as vc
from pygame import mixer
from threading import Thread, Event
import uuid

event = Event()
ALARMS = []
mixer.init()
alarm = mixer.music
alarm.load('mixkit-sleepy-cat-135.mp3')


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


def silence():
    alarm.stop()
    event.set()
    for a in ALARMS:
        if a["status"] == "ringing":
            a["status"] = "disabled"
    return


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
    minute = curr_time.tm_min + 5
    hour = curr_time.tm_hour
    if minute >= 60:
        hour += 1
        minute = minute % 60
        if hour >= 24:
            hour = hour % 24
    create((hour, minute))
    return


if __name__ == '__main__':
    try_ring()
    print("done")
