from flask import Flask, jsonify, request
from flask_cors import CORS
import alarm

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})


@app.route('/alarm', methods=['GET', 'DELETE', 'POST'])
def play_alarm():
    response_object = {'status': 'success'}
    if request.method == "GET":
        response_object["alarms"] = alarm.get_alarms()
    elif request.method == "POST":
        post_data = request.get_json()
        if post_data.get("action") == "start":
            alarm.try_ring()
        elif post_data.get("action") == "silence":
            alarm.silence()
        elif post_data.get("action") == "snooze":
            alarm.snooze()
        elif post_data.get("action") == "create":
            new_alarm = post_data.get("time").split(":")
            alarm.create(new_alarm)
        response_object["action"] = post_data.get("action")
    return jsonify(response_object)


@app.route('/alarm/<alarm_id>', methods=['DELETE'])
def single_alarm(alarm_id):
    response_object = {'status': 'success'}
    if request.method == "DELETE":
        alarm.delete(alarm_id)
    return jsonify(response_object)


if __name__ == '__main__':
    app.run()
