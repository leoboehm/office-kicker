from flask import Flask, jsonify, request, render_template

app = Flask(__name__)

motion_state = {'motion': False}

# render template based on motion state
@app.route("/")
def index():
    if get_motion() == True:
        return render_template("occupied.html")
    else:
        return render_template("unoccupied.html")

# return current motion state
@app.route('/motion', methods=['GET'])
def get_motion():
    return jsonify(motion_state)

# raspi endpoint to set the current motion state
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
