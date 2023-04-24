import time

alarms = {(5, 12), (15, 44), (15, 45), (22, 21)}
silenced_alarms = set()


def do_trigger_alarm():
    curr_time = time.localtime()
    if (curr_time.tm_hour, curr_time.tm_min) in alarms:  # set alarm time
        silenced_alarms.add((curr_time.tm_hour, curr_time.tm_min))
        alarms.remove((curr_time.tm_hour, curr_time.tm_min))
        return True
    return False
