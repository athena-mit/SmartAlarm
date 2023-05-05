import datetime

# Alarm status codes, used here instead of Enum for ease of autocomplete
ACTIVE = 'active'
RINGING = 'ringing'
DISABLED = 'disabled'
# Alarm modes, used here instead of Enum for ease of autocomplete
NO_ALARM = -1
QUE_SERA_SERA = 0
BASIC = 1
PASSIVE_AGGRESSIVE = 2
AT_ALL_COSTS = 3
MODES = {'que_sera_sera': QUE_SERA_SERA, 'basic': BASIC,
         'passive_aggressive': PASSIVE_AGGRESSIVE, 'at_all_costs': AT_ALL_COSTS}
# Event importance to alarm mode mapping
SEVERITY = {'high': AT_ALL_COSTS, 'medium': PASSIVE_AGGRESSIVE, 'low': BASIC, 'zero': QUE_SERA_SERA}


def convert_date_str_to_datettime(date):
    date_info = date.split(":")
    return datetime.datetime(*date_info)

def convert_date_str_to_datettime(date):
    date_info = date.split(":")
    return datetime.datetime(*date_info)


def convert_str_to_t_tup(time_string):
    return tuple(time_string.split(":"))


def correct_time(t):
    hour, minute = t
    if minute >= 60:
        hour += 1
        minute = minute % 60
        if hour >= 24:
            hour = hour % 24
    return hour, minute


def increase_time_by(t, num_minutes):
    hour, minute = t
    minute += num_minutes
    return correct_time((hour, minute))


def is_after(time1, time2):
    hour1, min1 = time1
    hour2, min2 = time2
    if hour1 < hour2 or (hour1 == hour2 and min1 < min2):
        return True
    return False
