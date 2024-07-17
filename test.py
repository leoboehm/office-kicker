import time
import threading
import requests
from flask import Flask, jsonify, request
from flask.testing import FlaskClient

# copy flask app for testing
app = Flask(__name__)

motion_state = {'motion': False}

@app.route('/motion', methods=['POST'])
def update_motion():
    global motion_state
    data = request.json
    if 'motion' in data:
        motion_state['motion'] = data['motion']
        print(f"Motion state updated: {motion_state['motion']}")
        return jsonify(success=True), 200
    else:
        return jsonify(success=False, error="Invalid data"), 400

@app.route('/motion', methods=['GET'])
def get_motion():
    return jsonify(motion_state)

# simulate raspi changing motion state
def simulate_raspi():
    while True:
        # simulate motion detection (changes on every call)
        motion_detected = not motion_state['motion']
        motion_state['motion'] = motion_detected
        # repeat every 2secs
        time.sleep(2)


if __name__ == "__main__":
    # create test client for flask app
    client = app.test_client()

    # start console thread to simulate the raspi behavior
    simulation_thread = threading.Thread(target=simulate_raspi)
    simulation_thread.start()

    try:
        # simulate interaction between raspi script and flask server
        while True:
            time.sleep(1)
            # get current motion state
            response = client.get('/motion')
            data = response.get_json()
            current_motion_state = data['motion']
            print(f"Current motion state: {current_motion_state}")

            # simulate raspi sending changed motion state data
            if current_motion_state != motion_state['motion']:
                try:
                    requests.post('/motion', json={'motion': motion_state['motion']})
                except Exception as e:
                    print(f"Failed to send data: {e}")

    except KeyboardInterrupt:
        print("Test interrupted")
        simulation_thread.join()
        print("Simulation thread stopped")
