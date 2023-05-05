import datetime
from alarm_schedule import AlarmSchedule
from event_calendar import EventCalendar
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

    def get_events(self, date):
        date_key = datetime.datetime.fromisoformat(date)
        date_key = date_key.replace(hour=0, minute=0, second=0)
        return self.events.get_day(date_key)

    def get_event_summary(self, date):
        date = datetime.datetime.fromisoformat(date)
        return self.events.get_calendar_summary(date.year, date.month)

    def add_alarm(self, time_str, mode_str='basic'):
        current_time = datetime.datetime.now()
        print("time info:" + str(time_str.split(":")))
        time_info = time_str.split(":")
        alarm_time = current_time.replace(hour=int(time_info[0]), minute=int(time_info[1]), second=0)
        print("alarm time =" + str(alarm_time))
        if alarm_time < current_time:
            tomorrow = alarm_time + datetime.timedelta(hours=24)
            print("tomorrow =" + str(tomorrow))
            return self.alarms.add(tomorrow, MODES[mode_str])
        return self.alarms.add(alarm_time, MODES[mode_str])

    def add_event(self, name, importance, s_time, e_time, w_time):
        date = datetime.datetime.fromisoformat(s_time)
        date = date.replace(hour=0, minute=0, second=0)
        return self.events.add(
            date,
            name,
            importance,
            datetime.datetime.fromisoformat(s_time),
            datetime.datetime.fromisoformat(e_time),
            datetime.datetime.fromisoformat(w_time)
        )

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
