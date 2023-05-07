import datetime

# Alarm status codes, used here instead of Enum for ease of autocomplete
ACTIVE = 'active'
RINGING = 'ringing'
DISABLED = 'disabled'
# Alarm modes, used here instead of Enum for ease of autocomplete
NO_ALARM = 'no_alarm'
QUE_SERA_SERA = 'que_sera_sera'
BASIC = 'basic'
PASSIVE_AGGRESSIVE = 'passive_aggressive'
AT_ALL_COSTS = 'at_all_costs'
MODE_DEGREE = {
    NO_ALARM: 0,
    QUE_SERA_SERA: 1,
    BASIC: 2,
    AT_ALL_COSTS: 3
}
# Event importance to alarm mode mapping
EVENT_MODE = {'high': AT_ALL_COSTS, 'medium': PASSIVE_AGGRESSIVE, 'low': BASIC, 'zero': QUE_SERA_SERA}


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
