# Smart Alarm
A multi-modal alarm system that allows users to silence their
alarm in three different ways:
1. Maintaining eye-contact with the system's camera for some
predetermined amount of time (~5 seconds depending on speed 
of processor)
**OR**
2. Verbally instructing the system to "silence alarm" or
"snooze alarm"
**OR**
3. Manually pressing the "Off" or "Snooze" button on the system's GUI

Additionally, the system provides a custom calendar for users to create
events, which will then schedule an alarm to wake them up at the specified time.


## Run
This project was written in Python 3.10.11 and Node v18.16.0, 
both will need to be installed in order to run the project. I
ran this on Windows 11, but it should work fine for Windows
10 as well. 

#### Running the backend
Run the following code in your terminal:
```
flask run --port=5001 --debug 
```
#### Running the frontend
Run the following code in a second terminal:
```
cd gui
npm install
npm run dev 
```
Follow link to local webpage (should be http://localhost:5173/)
Keep both terminals running at the same time for
the app to work properly. 

## Code Overview
The frontend portion of the app is contained in the 
[gui directory](/gui), all other files and directories are
part of the backend.

*Notes About the Frontend:*
* written using Vue Framework (Node version v18.16.0)
* All the non-automatically generated files are in the 
[gui/src directory](/gui/src). 
* For those unfamiliar with Vue, the [src/views](/gui/src/views) directory 
is used to simulate the different "pages" of the app for each route 
defined in [src/router/index.js](/gui/src/router/index.js). The other
directory worth noting is [src/components](/gui/src/components) which, as
the name implies, contains smaller components used by the files in [src/views](/gui/src/views). 

*Notes About the Backend:*
* written entirely in Python 3.10 (all external packages can
be viewd in [requirements.txt](/requirements.txt)).
* [app.py](/app.py) handles routing and requests from the
frontend. All of its computation is handled by [smart_alarm.py](/smart_alarm.py)
* [smart_alarm.py](/smart_alarm.py) contains the `SmartAlarm` class, which
acts as one master coordinator or "Manager" that brings together 
all other backend files.
* [utilities.py](/utilities.py) contains important constants shared
by the `AlarmSchedule`, `EventCalendar`, and `SmartAlarm` classes.

### Alarms
* *Frontend:* [AlarmView.vue](/gui/src/views/AlarmView.vue) allows
users to view and schedule alarms, in addition to silencing and snoozing
whichever alarm(s) are currently playing. [AlarmList.vue](/gui/src/components/AlarmList.vue)
allows users to delete individual alarms.
* [alarm_schedule.py](/alarm_schedule.py) contains the `AlarmSchedule` class,
which [smart_alarm.py](/smart_alarm.py) uses to keep and edit records of
alarms created by the user.
* The `SmartAlarm` class in [smart_alarm.py](/smart_alarm.py) is what actually
controls the alarm's ringing and initiates separate threads for alertness detection
and vocal commands.

#### Alertness Detection
The following files and folders are used in order to detect the 
user's face and determine if they are "alert enough" to silence 
the alarm. All the files/folders below were written by and downloaded
from [DataFlair](https://data-flair.training/blogs/python-project-driver-drowsiness-detection-system/) 
except for `alertness_detection.py`, which is a slight modification of the original
`drowsiness detection.py` that DataFlair provides; everything else was left unchanged.
* [haar cascade files/](/haar%20cascade%20files)
  * Contains three separate files which the system uses to identify
  faces in the camera feed and determine where its left and right eyes
  are.
* [models/](/models)
  * Contains the CNN model `cnnCat2.h5`, which determines if eyes are
  "Open" or "Closed"
* [model.py](/model.py)
  * Used to build the model in the `models/` directory. Not
  actually run at any point by the system, but left here for better
  understanding of how the model was created.
* [alertness_detection.py](/alertness_detection.py)
  * Initializes the camera feed and then combines the haar cascade files 
  and the CNN model to find the user's eyes, if present, and keep the camera
  running until the eyes have stayed open for the specified amount of time or
  until the user has snoozed/silenced the alarm through one of the other modalities.
#### Vocal Interaction
[voice_commands.py](/voice_commands.py) allows the system to listen
for voice commands and issue vocal confirmation to the user. File adapted
from example code by [GeeksForGeeks](https://www.geeksforgeeks.org/python-convert-speech-to-text-and-text-to-speech/).

### Events

* *Frontend:* [CalendarView.vue](/gui/src/views/CalendarView.vue) allows
users to see a summary of the month's calendar and create new events. 
[DayEvents.vue](/gui/src/components/DayEvents.vue) allows users to see the
details for the events on a particular day.
* [event_calendar.py](/event_calendar.py) contains the `EventCalendar`
class, which [smart_alarm.py](/smart_alarm.py) uses to keep and edit
records of events created by the user.

### Virtual Room

* *Frontend:* [RoomView.vue](/gui/src/views/RoomView.vue) allows users
to view the state of the virtual room and reset it whenever they wish.
* [virtual_room.py](/virtual_room.py) contains the `VirtualRoom` class,
which allows [smart_alarm.py](/smart_alarm.py) to make the appropriate
adjustments to the virtual room's settings in response to certain user
actions (ex. increasing user brightness when a 'Passive Aggressive' alarm
is snoozed).