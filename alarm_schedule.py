import datetime
import uuid
from utilities import *


class AlarmSchedule:
    __records = []
    __severest_ringing_alarm = NO_ALARM

    def add(self, t: datetime.datetime, mode: int):
        for a in self.__records:
            if a['status'] == ACTIVE and a['time'] == t:
                return False
        self.__records.append({
            'id': uuid.uuid4().hex,
            'time': t,
            'status': ACTIVE,
            'mode': mode
        })
        return True

    def remove(self, alarm_id):
        for a in self.__records:
            if a['id'] == alarm_id:
                self.__records.remove(a)
                return True
        return False

    def get_current_mode(self):
        return self.__severest_ringing_alarm

    def get_all(self):
        return self.__records.copy()

    def silence(self):
        for a in self.__records:
            if a['status'] == RINGING:
                a['status'] = DISABLED
        self.__severest_ringing_alarm = NO_ALARM
        return

    def is_time_to_trigger(self):
        t = datetime.datetime.now()
        alarm_mode = NO_ALARM
        for a in self.__records:
            if a['status'] == ACTIVE and a['time'] <= t:
                a['status'] = RINGING
                if a['mode'] > alarm_mode:
                    alarm_mode = a['mode']
        if alarm_mode > self.__severest_ringing_alarm:
            if self.__severest_ringing_alarm != NO_ALARM:
                # another alarm is already ringing
                self.__severest_ringing_alarm = alarm_mode
                return False
            self.__severest_ringing_alarm = alarm_mode
            return True
        return False
