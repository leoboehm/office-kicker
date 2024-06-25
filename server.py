from flask import Flask, jsonify, render_template_string
from datetime import datetime, timedelta

app = Flask(__name__)
timestamp = None

@app.route('/motion', methods=['GET'])
def set_motion_timestamp():
    global timestamp
    timestamp = datetime.now()
    return jsonify({"message": "Timestamp set", "timestamp": timestamp}), 200

@app.route('/get_motion', methods=['GET'])
def get_motion_timestamp():
    global timestamp
    if timestamp is None:
        return render_template_string('<h1>No motion detected</h1>')
    else:
        return render_template_string('<h1>Motion detected!</h1>')