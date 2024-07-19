from flask import Flask, jsonify, render_template
from datetime import datetime

app = Flask(__name__)

timestamp = None

# render ui template based on motion activity
@app.route("/")
def index():
    if get_motion_timedout():
        return render_template("unoccupied.html")
    else:
        return render_template("occupied.html")
    
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
    delta = timestamp - datetime.now()
    delta = datetime.now() - timestamp
    if delta.total_seconds() > 120:
        return True
    # recent motion activity detected
    return False

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3000)
