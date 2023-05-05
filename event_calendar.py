from enum import Enum
import uuid
import datetime
from utilities import *
import calendar


class EventCalendar:
    __records = {}

    def add(self, date, name, importance, t_start, t_end, t_warn):
        event = {
            "id": uuid.uuid4().hex,
            'name': name,
            'importance': importance,
            'start_time': t_start,
            'end_time': t_end,
            'warn_time': t_warn
        }
        if date in self.__records.keys():
            self.__records[date].append(event)
        else:
            self.__records[date] = [event]
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
        if date not in self.__records.keys():
            return False
        return self.__records[date].copy()

    def get_calendar_summary(self, year, month):
        summary = []
        for i in range(1, calendar.monthrange(year, month)[1] + 1):
            date = datetime.datetime(year=year, month=month, day=i, hour=0, minute=0, second=0)
            if date in self.__records.keys():
                summary.append(len(self.__records[date]))
            else:
                summary.append(0)
        return summary


    def get_range(self, start_date: str, end_date: str) -> dict:
        mini_calendar = []
        current_key = convert_date_str_to_datettime(start_date)
        end_key = convert_date_str_to_datettime(end_date)
        while current_key <= end_key:
            day_cal = {
                'date': str(current_key.month) + "/" + str(current_key.day),
                'weekday': current_key.isoweekday(),
                'events': []
            }
            if current_key in self.__records.keys():
                day_cal['events'] = self.__records[current_key].copy()
            mini_calendar.append(day_cal)
            current_key += datetime.timedelta(days=1)
        return mini_calendar

    def get_soonest_event(self):
        curr_date_key = datetime.datetime.now()
        curr_time = (curr_date_key.hour, curr_date_key.minute)
        soonest_event = None
        soonest_time = None
        if curr_date_key in self.__records.keys():
            for e in self.__records[curr_date_key]:
                event_time = convert_str_to_t_tup(e.start_time)
                if is_after(event_time, curr_time) and \
                        (not soonest_event or is_after(soonest_time, event_time)):
                    soonest_time = event_time
                    soonest_event = e
        if not soonest_event:
            next_date_key = curr_date_key + datetime.timedelta(days=1)
            if next_date_key in self.__records.keys():
                event_time = convert_str_to_t_tup(e.start_time)
                for e in self.__records[next_date_key]:
                    if not soonest_event or is_after(soonest_time, event_time):
                        soonest_time = event_time
                        soonest_event = e
        return soonest_event.copy()
