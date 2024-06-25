from flask import Flask, jsonify, render_template_string, render_template
from datetime import datetime

app = Flask(__name__)

timestamp = None

# render ui template based on motion activity
@app.route("/")
def index():
    if get_motion_timedout():
        return render_template("sleepMode.html")
    else:
        return render_template("actionMode.html")

# set last motion timestamp
@app.route('/motion', methods=['GET'])
def set_motion_timestamp():
    global timestamp
    timestamp = datetime.now()
    return jsonify({"message": "Timestamp set", "timestamp": timestamp}), 200


# check for recent motion activity
def get_motion_timedout():
    global timestamp
    # no motion activity detected
    if timestamp is None:
        return True
    # last motion activity was longer than 5min ago
    delta = datetime.now() - timestamp
    print(delta.total_seconds())
    if delta.total_seconds() > 300:
        return True
    # recent motion activity detected
    return False