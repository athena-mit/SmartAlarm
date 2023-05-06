import datetime
import json

from flask import Flask, jsonify, request
from flask_cors import CORS
from smart_alarm import SmartAlarm

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})

MANAGER = SmartAlarm()


@app.route('/alarm', methods=['GET', 'DELETE', 'POST'])
def play_alarm():
    response_object = {'status': 'success'}
    if request.method == "GET":
        response_object["alarms"] = MANAGER.get_alarms()
        response_object['brightness'] = MANAGER.get_room_brightness();
    elif request.method == "POST":
        post_data = request.get_json()
        if post_data.get("action") == "start":
            MANAGER.try_ring()
        elif post_data.get("action") == "silence":
            MANAGER.silence()
        elif post_data.get("action") == "snooze":
            MANAGER.try_snooze()
        elif post_data.get("action") == "create":
            MANAGER.add_alarm(post_data.get("time"))
        response_object["action"] = post_data.get("action")
    return jsonify(response_object)


@app.route('/alarm/<alarm_id>', methods=['DELETE'])
def single_alarm(alarm_id):
    response_object = {'status': 'success'}
    if request.method == "DELETE":
        MANAGER.delete_alarm(alarm_id)
    return jsonify(response_object)


@app.route('/event/<date>', methods=['GET'])
def get_events(date):
    return jsonify({'status': 'success', "events": MANAGER.get_events(date)})


@app.route('/event/summary/<date>', methods=['GET'])
def get_summary(date):
    return jsonify({'status': 'success', "events": MANAGER.get_event_summary(date)})


@app.route('/event', methods=['GET', 'POST'])
def handle_events():
    response_object = {'status': 'success'}
    if request.method == "POST":
        post_data = request.get_json()
        if post_data.get("action") == "create":
            MANAGER.add_event(
                post_data.get("name"),
                post_data.get("importance"),
                post_data.get("start_time"),
                post_data.get("end_time"),
                post_data.get("warn_time")
            )
        response_object["action"] = post_data.get("action")
    return jsonify(response_object)


@app.route('/room', methods=['GET'])
def handle_room():
    return jsonify({'status': 'success', "brightness": MANAGER.get_room_brightness()})


if __name__ == '__main__':
    app.run()
