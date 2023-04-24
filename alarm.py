import time
import alertness_detection as ad

alarms = {(5, 12), (23, 22), (23, 23), (23, 24), (23, 25), (23, 26)}
silenced_alarms = set()

current_alarm = (0, 0)


def get_alarms():
    return list(alarms)


def create(new_alarm):
    alarms.add((int(new_alarm[0]), int(new_alarm[1])))
    return


def do_trigger_alarm():
    global current_alarm
    curr_time = time.localtime()
    if (curr_time.tm_hour, curr_time.tm_min) in alarms:  # set alarm time
        current_alarm = (curr_time.tm_hour, curr_time.tm_min)
        silenced_alarms.add(current_alarm)
        alarms.remove(current_alarm)
        return True
    return False


def try_ring():
    if do_trigger_alarm():
        ad.trigger_alarm()
    return


def silence():
    ad.silence_alarm()
    return


def snooze():
    ad.silence_alarm()
    hrs, mins = current_alarm
    mins += 5
    if mins >= 60:
        hrs += 1
        mins = mins % 60
        if hrs >= 24:
            hrs = hrs % 24
    alarms.add((hrs, mins))
    return
