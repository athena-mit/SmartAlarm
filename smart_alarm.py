import datetime
from a_class import AlarmSchedule
from e_class import EventCalendar
from utilities import *
import alertness_detection as ad
import voice_commands as vc
from pygame import mixer
from threading import Thread, Event


class SmartAlarm:
    alarms = AlarmSchedule()
    events = EventCalendar()
    mixer.init()
    ringtone = mixer.music
    ringtone.load('mixkit-sleepy-cat-135.mp3')
    ring_event = Event()

    def get_alarms(self):
        return self.alarms.get_all()

    def add_alarm(self, time_str, mode_str='basic'):
        time_info = time_str.split(":")
        hour, minute = int(time_info[0]), int(time_info[1])
        current_time = datetime.datetime.now()
        current_time.replace(second=0)
        if hour < current_time.hour or (hour == current_time.hour and minute < current_time.minute):
            tomorrow = current_time + datetime.timedelta(days=1)
            return self.alarms.add(tomorrow, MODES[mode_str])
        return self.alarms.add(current_time, MODES[mode_str])

    def delete_alarm(self, alarm_id):
        return self.alarms.remove(alarm_id)

    def silence(self):
        self.ringtone.stop()
        self.ring_event.set()
        self.alarms.silence()
        return

    def try_ring(self):
        if self.alarms.is_time_to_trigger():
            self.ring_event.clear()
            camera_detection = Thread(target=ad.trigger_alarm, args=(self.ring_event,))
            vocal_command = Thread(target=vc.get_voice_command, args=(self.ring_event,))
            self.ringtone.play(loops=-1)
            camera_detection.start()
            vocal_command.start()
            self.ring_event.wait()
            self.ringtone.stop()
            camera_detection.join()
            vocal_command.join()
        return

    def __schedule_next_alarm(self, snooze=0):
        snooze_mode = self.alarms.get_current_mode()
        snooze_time = datetime.datetime.now() + datetime.timedelta(minutes=snooze)
        soonest_event = self.events.get_soonest_event()
        if soonest_event and (not snooze or soonest_event['warn_time'] <= snooze_time):
            return self.alarms.add(
                soonest_event['warn_time'],
                max(SEVERITY[soonest_event['importance']], snooze_mode)
            )
        return self.alarms.add(snooze_time, snooze_mode)

    def try_snooze(self, minutes="5"):
        snooze_mode = self.alarms.get_current_mode()
        if snooze_mode == AT_ALL_COSTS:
            vc.speak_text("Snoozing is not allowed. You must wake up.")
            return False
        elif snooze_mode == NO_ALARM:
            vc.speak_text("No alarm is ringing. Cannot snooze.")
            return False
        self.__schedule_next_alarm(int(minutes))
        self.silence()
        return True


