import time
import alertness_detection as ad
import voice_commands as vc
from pygame import mixer
from multiprocessing import Process, Event

mixer.init()
alarm = mixer.music
alarm.load('mixkit-sleepy-cat-135.mp3')

alarm_times = {(23, 22), (23, 23), (23, 24), (23, 25), (23, 26)}
silenced_alarms = set()

event = Event()


def get_current_time():
    curr_time = time.localtime()
    return curr_time.tm_hour, curr_time.tm_min


def get_times():
    return list(alarm_times)


def create(new_alarm):
    alarm_times.add((int(new_alarm[0]), int(new_alarm[1])))
    return


def do_trigger_alarm():
    current_time = get_current_time()
    if current_time in alarm_times:  # set alarm time
        silenced_alarms.add(current_time)
        alarm_times.remove(current_time)
        return True
    return False


# def camera_detection(event):
#     ad.trigger_alarm(event)
#     event.set()
#     return
#
#
# def voice_detection(event):
#     commainvc.get_voice_command(event)
#     event.is_set()
#     return

def try_ring():
    global alarm, event
    if do_trigger_alarm() or True:
        event.clear()
        camera_detection = Process(target=ad.trigger_alarm, args=(event,))
        vocal_command = Process(target=vc.get_voice_command, args=(event,))
        alarm.play(loops=-1)
        camera_detection.start()
        vocal_command.start()
        camera_detection.join()
        vocal_command.join()
        silence()
    return


def silence():
    alarm.stop()
    event.set()
    return


def snooze():
    silence()
    hrs, minutes = get_current_time()
    minutes += 5
    if minutes >= 60:
        hrs += 1
        minutes = minutes % 60
        if hrs >= 24:
            hrs = hrs % 24
    alarm_times.add((hrs, minutes))
    return


if __name__ == '__main__':
    try_ring()
    print("done")
