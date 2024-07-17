from flask import Flask, jsonify, request, render_template
from datetime import datetime

app = Flask(__name__)

motion_state = {'motion': False}

@app.route("/")
def index():
    if get_motion() == True:
        return render_template("actionMode.html")
    else:
        return render_template("sleepMode.html")

@app.route('/motion', methods=['GET'])
def get_motion():
    return jsonify(motion_state)

@app.route('/motion', methods=['POST'])
def update_motion():
    global motion_state
    data = request.json
    if 'motion' in data:
        motion_state['motion'] = data['motion']
        return jsonify(success=True), 200
    else:
        return jsonify(success=False, error="Invalid data"), 400

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3000)
