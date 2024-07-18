### Building a Smart Foosball Table with Raspberry Pi

In this blog post, I'll walk you through creating a smart foosball table using a Raspberry Pi 3, a motion sensor, and LED strips. This project will detect whether the table is in use and display the occupancy status on a web page. Additionally, LED strips will light up when the table is occupied and turn off when it's not. Let's dive into the step-by-step process.

#### Materials Needed

1. Raspberry Pi 3 (with Raspbian installed)
2. PIR motion sensor
3. LED strips
4. Breadboard and jumper wires
5. 5V power supply (for the LED strips)
6. Internet connection for the Raspberry Pi

#### Step 1: Setting Up the Hardware

**1. Connect the Motion Sensor to the Raspberry Pi**

The PIR motion sensor typically has three pins: VCC, GND, and OUT.

- Connect the VCC pin to the 5V pin on the Raspberry Pi.
- Connect the GND pin to a GND pin on the Raspberry Pi.
- Connect the OUT pin to GPIO pin 17 on the Raspberry Pi (or any other GPIO pin of your choice).

**2. Connect the LED Strips**

- Connect the positive terminal of the LED strip to a 5V power supply.
- Connect the ground terminal of the LED strip to a GND pin on the Raspberry Pi.
- Connect the data input of the LED strip to GPIO pin 18 on the Raspberry Pi (or any other GPIO pin of your choice).

#### Step 2: Setting Up the Software

**1. Update and Upgrade the Raspberry Pi**

```sh
sudo apt-get update
sudo apt-get upgrade
```

**2. Install Flask**

```sh
sudo apt-get install python3-flask
```

**3. Install GPIO Library**

```sh
sudo apt-get install python3-rpi.gpio
```

#### Step 3: Writing the Python Script

Create a Python script to handle motion detection and LED control. Let's call it `foosball.py`.

```python
import RPi.GPIO as GPIO
import time
from flask import Flask, render_template

app = Flask(__name__)

# GPIO setup
PIR_PIN = 17
LED_PIN = 18

GPIO.setmode(GPIO.BCM)
GPIO.setup(PIR_PIN, GPIO.IN)
GPIO.setup(LED_PIN, GPIO.OUT)

@app.route('/')
def index():
    if GPIO.input(PIR_PIN):
        GPIO.output(LED_PIN, GPIO.HIGH)
        return render_template('occupied.html')
    else:
        GPIO.output(LED_PIN, GPIO.LOW)
        return render_template('unoccupied.html')

if __name__ == '__main__':
    try:
        app.run(host='0.0.0.0', port=5000)
    except KeyboardInterrupt:
        print("Exiting")
    finally:
        GPIO.cleanup()
```

#### Step 4: Creating HTML Templates

Create two HTML files: `occupied.html` and `unoccupied.html`.

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

#### Step 5: Running the Flask Application

Run your Flask application with the following command:

```sh
python3 foosball.py
```

Your Flask application will start, and you can view the occupancy status by navigating to the Raspberry Pi's IP address on port 5000 using a web browser.

#### Step 6: Testing the Setup

- Place the motion sensor in a position where it can detect movement near the foosball table.
- When motion is detected, the LED strips should light up, and the web page should display "The foosball table is occupied!"
- When no motion is detected, the LED strips should turn off, and the web page should display "The foosball table is unoccupied!"

#### Conclusion

Congratulations! You've successfully built a smart foosball table using a Raspberry Pi, a motion sensor, and LED strips. This project not only enhances the fun of playing foosball but also provides a practical application of integrating hardware with web technologies.

Feel free to customize the project further, such as adding more features or improving the web interface. Happy hacking!