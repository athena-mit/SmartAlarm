from flask import Flask, jsonify, request
from flask_cors import CORS
import time
# from check_alarm import do_trigger_alarm
import alertness_detection as ad



# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})

# mixer.init()
# alarm = mixer.music
# alarm.load('mixkit-sleepy-cat-135.mp3')

alarms = {(5, 12), (23, 22), (23, 23), (23, 24), (23, 25), (23, 26)}
silenced_alarms = set()


def do_trigger_alarm():
    curr_time = time.localtime()
    if (curr_time.tm_hour, curr_time.tm_min) in alarms:  # set alarm time
        silenced_alarms.add((curr_time.tm_hour, curr_time.tm_min))
        alarms.remove((curr_time.tm_hour, curr_time.tm_min))
        return True
    return False


# sanity check route
@app.route('/alarm', methods=['GET', 'POST'])
def play_alarm():
    response_object = {'status': 'success'}
    # if request.method == "GET":
    #     alarm.play(loops=-1)
    #     trigger_alarm()
    if request.method == "POST":
        post_data = request.get_json()
        if post_data.get("action") == "start":
            if do_trigger_alarm():
                # alarm.play(loops=-1)
                ad.trigger_alarm()
        elif post_data.get("action") == "silence":
            # alarm.stop()
            ad.silence_alarm()

        # alarm.stop()
        response_object["action"] = post_data.get("action")
    return jsonify(response_object)


if __name__ == '__main__':
    app.run()
