import datetime
import time

from alarm_schedule import AlarmSchedule
from event_calendar import EventCalendar
from virtual_room import VirtualRoom
from utilities import *
import alertness_detection as ad
import voice_commands as vc
from pygame import mixer
from threading import Thread, Event


class SmartAlarm:
    alarms = AlarmSchedule()
    events = EventCalendar()
    room = VirtualRoom()
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

    def get_room_brightness(self):
        return self.room.get_brightness()

    def add_alarm(self, time_str, mode='basic'):
        current_time = datetime.datetime.now()
        current_time = current_time.replace(second=0)
        time_info = time_str.split(":")
        alarm_time = current_time.replace(hour=int(time_info[0]), minute=int(time_info[1]))
        if alarm_time < current_time:
            tomorrow = alarm_time + datetime.timedelta(hours=24)
            return self.alarms.add(tomorrow, mode)
        return self.alarms.add(alarm_time, mode)

    def add_event(self, name, importance, s_time, e_time, w_time):
        self.alarms.add(
            datetime.datetime.fromisoformat(w_time),
            EVENT_MODE[importance]
        )
        return self.events.add(
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
            event_timeout = None
            camera_detection = Thread(target=ad.trigger_alarm, args=(self.ring_event,))
            vocal_command = vc.VoiceCommands(
                self.ring_event,
                self.alarms.get_current_mode() != AT_ALL_COSTS
            )
            camera_detection.start()
            vocal_command.start()
            self.ringtone.play(loops=-1)
            if self.alarms.get_current_mode() == AT_ALL_COSTS:
                self.room.max_brightness()
            elif self.alarms.get_current_mode() == QUE_SERA_SERA:
                event_timeout = 60
            self.ring_event.wait(timeout=event_timeout)
            if not self.ring_event.is_set():
                self.ring_event.set()
            self.ringtone.stop()
            camera_detection.join()
            vocal_command.join()
            if vocal_command.command_is_snooze:
                self.try_snooze()
            else:
                self.alarms.silence()
        return

    def try_snooze(self, minutes="1"):
        snooze_mode = self.alarms.get_current_mode()
        if snooze_mode == AT_ALL_COSTS:
            vc.speak_text("Snoozing is not allowed. You must wake up.")
            return False
        elif snooze_mode == NO_ALARM:
            vc.speak_text("No alarm is ringing. Cannot snooze.")
            return False
        elif snooze_mode == PASSIVE_AGGRESSIVE:
            self.room.increase_brightness()
        self.alarms.snooze(int(minutes))
        self.silence()
        return True

    def reset_room(self):
        return self.room.turn_off_lights()
