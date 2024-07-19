# Building a Smart Foosball Table with Raspberry Pi

Maybe you have a foosball table in your office or club and want to know if someone is currently playing without having to leave your seat, or you're just searching for your next fun DIY-project - anyways, I got you.
In this beginners tutorial, I'll walk you through the steps of creating a smart foosball table using a Raspberry Pi 3, a motion sensor and a Flask server. In the end, the system will detect whether the table is in use and display the occupancy status on a web page. As an additional fun feature, LED strips will light up when the table is occupied.

Enough explanation, let's dive into it!

Note: I used Codesphere as an external server to host the flask app, it is totally possible to host the app on any chosen platform or even directly on your microcontroller.


## Materials Needed

1. Raspberry Pi 3 (with Raspbian installed)
2. PIR motion sensor
3. LED strips
4. Breadboard and jumper wires
5. 5V power supply (for the LED strips)

Note: Your Raspberry Pi needs an internet connection to send the motion data to the server. I simply connected it via WLAN, otherwise you would need to ensure connection via a LAN cable which is rather inconvenient for the foosball table setup.

## Step 1: Setting Up the Hardware

**1. Connect the Motion Sensor to the Raspberry Pi**

The PIR motion sensor typically has three pins: VCC, GND, and OUT.

- Connect the VCC pin to the 5V pin on the Raspberry Pi.
- Connect the GND pin to a GND pin on the Raspberry Pi.
- Connect the OUT pin to GPIO pin 17 (= pin 11 on the Raspberry Pi) or any other GPIO pin of your choice.

**2. Connect the LED Strips**

- Connect the positive terminal of the LED strip to a 5V power supply.
- Connect the ground terminal of the LED strip to a GND pin on the Raspberry Pi.
- Connect the data input of the LED strip to GPIO pin 18 (= pin 12 on the Raspberry Pi) or any other GPIO pin of your choice.

## Step 2: Writing the Python Script for the Raspberry Pi

**Before starting to code: Make sure the Raspberry Pi is updated and has the GPIO and requests libraries installed**

```sh
sudo apt-get update
sudo apt-get upgrade

sudo apt-get install python3-rpi.gpio

sudo apt-get install python3-requests
```

Create a Python script to handle motion detection, LED control, and communication with the external Flask server. Let's simply call it `kicker_pi.py`.

First, we need to import the libraries and configure the pin setup we previously chose. Since I am hosting the server on Codesphere, I also added the server url, but we'll get to this later.

```python
import RPi.GPIO as GPIO
import time
import requests

# GPIO setup
PIR_PIN = 17
LED_PIN = 18

GPIO.setmode(GPIO.BOARD)
GPIO.setup(PIR_PIN, GPIO.IN)
GPIO.setup(LED_PIN, GPIO.OUT)

# server url
SERVER_URL = 'https://<your_codesphere_url>.codesphere.com/motion'
```

Now, we can start implementing the function handling the incoming signal from the motion sensor.

```python
def detect_motion():
    while True:
        # check for motion
        if GPIO.input(PIR_PIN):
            try:
                # send motion state
                requests.get(SERVER_URL)
            except Exception as e:
                print(f"Failed to send data: {e}")
        else:
            pass
        
        # update every second
        time.sleep(1)
```

Since we also want to turn on LED strips when motion is detected, we expand our detect_motion function to send output signals to the connected LEDs. This is simply done by either sending HIGH (on) or LOW (off) to the GPIO pin.

```python
def detect_motion():
    while True:
        # check for motion
        if GPIO.input(PIR_PIN):
            # turn on LED
            GPIO.output(LED_PIN, GPIO.HIGH)
            try:
                # send motion state
                requests.get(SERVER_URL)
            except Exception as e:
                print(f"Failed to send data: {e}")
        else:
            # turn off LED
            GPIO.output(LED_PIN, GPIO.LOW)
        
        # update every second
        time.sleep(1)
```

Last but not least, we add the following lines to execute the function at the bottom of our file:

```python
if __name__ == "__main__":
    try:
        detect_motion()
    except KeyboardInterrupt:
        print("Quit")
        GPIO.cleanup()
```

Run the Raspberry Pi script with the following command:

```sh
python3 kicker_pi.py
```

## Step 3: Creating the Flask Application

**1. Install Flask**

```sh
pip install flask
```

**2. Create the Flask server**

Create a new file called `server.py`, import the necessary functions and libraries, and create a Flask app.

```python
from flask import Flask, jsonify, render_template
from datetime import datetime

app = Flask(__name__)
```

Next, we need to provide an endpoint for the Raspberry Pi to call on motion activity. This function should then set the current timestamp which we will use later on to check for recent activity.

```python
timestamp = None

# set last motion timestamp
@app.route('/motion', methods=['GET'])
def set_motion_timestamp():
    global timestamp
    timestamp = datetime.now()
    return jsonify({"message": "Timestamp set", "timestamp": timestamp}), 200

```

Now, we need a function to calculate the difference between the current timestamp and the last motion timestamp. I chose 2 minutes time difference, so if there was no activity for 2 minutes, the function will return false.

```python
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
```

Since we want to render different templates based on the current motion state, our index function needs to look like this:

```python
# render template based on motion state
@app.route("/")
def index():
    if get_motion_timedout() == True:
        return render_template("occupied.html")
    else:
        return render_template("unoccupied.html")
```

In the next step, we will create the templates. Before that, we have to add the function running the server to the bottom of the server.py file.
Since I am hosting on Codesphere, which is running on host 0.0.0.0 and port 3000, I set the parameters accordingly.

```python
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3000)
```

**3. Create the HTML Templates**

At the same root as your server.py file, create a directory called `templates` and add two HTML files: `occupied.html` and `unoccupied.html`. It is important that those files (or any template files) are placed inside this directory, otherwise Flask will not be able to find them.
The following are very basic examples of how those files might look, displaying the current occupancy state in a very simple heading. Feel free to further customise and enhance the HTML code to your liking.

**`occupied.html`**

```html
<!DOCTYPE html>
<html>
<head>
    <title>Foosball Table Status</title>
</head>
<body style="background-color: green; color: white; text-align: center;">
    <h1>The foosball table is occupied!</h1>
</body>
</html>
```

**`unoccupied.html`**

```html
<!DOCTYPE html>
<html>
<head>
    <title>Foosball Table Status</title>
</head>
<body style="background-color: red; color: white; text-align: center;">
    <h1>The foosball table is unoccupied!</h1>
</body>
</html>
```

**4. Set the Flask environment variables**

To get our Flask application to run, we need to specify environment variables. We need to set at least the `FLASK_APP` variable, to tell Flask which file to run. It needs to have the same name as the file containing your flask code, in our case `server`. Since I don't want to reset them on every server restart, I created an `.env` file:

```env
FLASK_APP=server
```

Other than that, Flask provides lots of different configuation variables, here are the most important:
- `FLASK_ENV` (prod by default, change to dev when running locally)
- `FLASK_RUN_HOST`
- `FLASK_RUN_PORT`

To ensure the environment variables are also read when deployed on the server, I added an `app.py` file, that imports the variales.

```python
from dotenv import load_dotenv

load_dotenv()
```

Run your Flask application with the following command:

```sh
python server.py
```

or directly via flask:

```sh
flask run
```

## Step 4 (optional): Hosting on Codesphere
1. Sign in with your Codesphere account or create an account.
2. Create a new workspace: Chose the repository you ant to deploy by connecting to either BitBucket, GitHub or GitLab. Select your preferred deployment mode and a payment plan based on the capacities you need.
3. Once the repository is set up in your workspace, make sure to install Flask and other software requirements as previously mentioned.
4. You should now be able to run your Flask server via the workspace's terminal.
5. Click "Open deployment" to navigate to your website. This is also where you find the server url needed in the Raspberry Pi script.

## Step 5: Finishing and testing the Setup

- Place the motion sensor in a position where it can detect movement near the foosball table.
- When motion is detected, the LED strips should light up, and the web page should display "The foosball table is occupied!"
- When no motion is detected, the LED strips should turn off, and the web page should display "The foosball table is unoccupied!"

## Conclusion

Congratulations! You've successfully built a smart foosball table using a Raspberry Pi, a motion sensor, LED strips, and a Flask server. This project provides a beginners entrypoint to the practical application of integrating hardware with web technologies.

Hopefully, I was able to inspire you, feel free to customize the project further, such as adding more features or improving the web interface!

You can find the full code at my [GitHub repository](https://github.com/leoboehm/office-kicker).