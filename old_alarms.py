# import time
# import alertness_detection as ad
# import voice_commands as vc
# from pygame import mixer
# from threading import Thread, Event
# import uuid
# from enum import Enum
# from utilities import *
# from events import get_soonest_event, Importance
#
# event = Event()
# ALARMS = []
# mixer.init()
# alarm = mixer.music
# alarm.load('mixkit-sleepy-cat-135.mp3')
# severest_ringing_alarm_mode = NO_ALARM
#
#
# def get_all():
#     return ALARMS.copy()
#
#
# def create(new_alarm, mode):
#     hour, minute = convert_str_to_t_tup(new_alarm)
#     for a in ALARMS:
#         if a["hour"] == hour and a["min"] == minute:
#             return False
#     ALARMS.append({
#         "id": uuid.uuid4().hex,
#         "hour": int(new_alarm[0]),
#         "min": int(new_alarm[1]),
#         "status": ACTIVE,
#         "mode": MODES[mode]
#     })
#     return True
#
#
# def delete(alarm_id):
#     for a in ALARMS:
#         if a["id"] == alarm_id:
#             ALARMS.remove(a)
#             return True
#     return False
#
#
# def silence():
#     global severest_ringing_alarm_mode
#     alarm.stop()
#     event.set()
#     severest_ringing_alarm_mode = NO_ALARM
#     for a in ALARMS:
#         if a["status"] == RINGING:
#             a["status"] = DISABLED
#     return
#
#
# def try_ring():
#     global severest_ringing_alarm_mode
#     curr_time = time.localtime()
#     alarm_mode = NO_ALARM
#     for a in ALARMS:
#         if a["hour"] == curr_time.tm_hour \
#                 and a["min"] == curr_time.tm_min \
#                 and a["status"] == ACTIVE and a['mode'] > alarm_mode:
#             a["status"] = RINGING
#             alarm_mode = a['mode']
#     if alarm_mode != NO_ALARM:
#         event.clear()
#         camera_detection = Thread(target=ad.trigger_alarm, args=(event,))
#         vocal_command = Thread(target=vc.get_voice_command, args=(event,))
#         alarm.play(loops=-1)
#         severest_ringing_alarm_mode = alarm_mode
#         camera_detection.start()
#         vocal_command.start()
#         event.wait()
#         alarm.stop()
#         camera_detection.join()
#         vocal_command.join()
#     return
#
#
# def try_snooze(t_min=5):
#     if severest_ringing_alarm_mode == AT_ALL_COSTS:
#         vc.speak_text("Snoozing is not allowed. You must wake up.")
#     elif severest_ringing_alarm_mode != NO_ALARM:
#         curr_time = time.localtime()
#         create(
#             increase_time_by(
#                 (curr_time.tm_hour, curr_time.tm_min),
#                 t_min
#             ),
#             severest_ringing_alarm_mode
#         )
#         silence()
#     # nothing happens if no alarm is ringing
#     return
#
#
# def schedule_next_alarm(snooze_time=None):
#     curr_time = time.localtime()
#     curr_time_tup = (curr_time.tm_hour, curr_time.tm_min)
#     soonest_event = get_soonest_event()
#     if soonest_event:
#         event_time = convert_str_to_t_tup(soonest_event)
#         if snooze_time and is_after(event_time, snooze_time):
#             create()
#         elif soonest_event['importance'] == Importance.HIGH.name:
#             create(event_time, Mode.AT_ALL_COSTS.name)
#         elif soonest_event['importance'] == Importance.MED.name:
#             create(event_time, Mode.BASIC.name)
#         else:
#             create(event_time, Mode.QUE_SERA_SERA)
#     return
#
#
# if __name__ == '__main__':
#     try_ring()
#     print("done")
