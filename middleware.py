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
