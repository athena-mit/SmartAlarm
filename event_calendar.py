from enum import Enum
import uuid
import datetime
from utilities import *
import calendar


class EventCalendar:
    __records = {}

    def add(self, name, importance, t_start, t_end, t_warn):
        date_key = t_start.replace(hour=0, minute=0, second=0)
        event = {
            "id": uuid.uuid4().hex,
            'name': name,
            'importance': importance,
            'start_time': t_start.replace(second=0),
            'end_time': t_end.replace(second=0),
            'warn_time': t_warn.replace(second=0)
        }
        if date_key in self.__records.keys():
            self.__records[date_key].append(event)
        else:
            self.__records[date_key] = [event]
        return

    def remove(self, date, event_id):
        date_key = convert_date_str_to_datettime(date)
        for e in self.__records[date_key]:
            if e['id'] == event_id:
                self.__records[date_key].remove(e)
                return True
        return False

    def get_all(self):
        return self.__records.copy()

    def get_day(self, date):
        date_key = date.replace(hour=0, minute=0, second=0)
        if date_key not in self.__records.keys():
            return False
        return self.__records[date_key].copy()

    def get_calendar_summary(self, year, month):
        summary = []
        for i in range(1, calendar.monthrange(year, month)[1] + 1):
            date = datetime.datetime(year=year, month=month, day=i, hour=0, minute=0, second=0)
            if date in self.__records.keys():
                summary.append(len(self.__records[date]))
            else:
                summary.append(0)
        return summary

    def get_soonest_event(self):
        current_time = datetime.datetime.now()
        today = current_time.replace(hour=0, minute=0, second=0, microsecond=0)
        soonest_event = None
        if today in self.__records.keys():
            for e in self.__records[today]:
                print("e: " + str(e))
                if e['warn_time'] > current_time and \
                        (not soonest_event or soonest_event['warn_time'] > e['warn_time']):
                    soonest_event = e
        if not soonest_event:
            next_date_key = today + datetime.timedelta(days=1)
            if next_date_key in self.__records.keys():
                for e in self.__records[next_date_key]:
                    if not soonest_event or soonest_event['warn_time'] > e['warn_time']:
                        soonest_event = e
            if not soonest_event:
                return False
        return soonest_event.copy()
