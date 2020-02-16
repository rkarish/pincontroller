from flask import Flask, render_template
from flask_simplelogin import SimpleLogin, login_required
import RPi.GPIO as GPIO


def create_app():
    app = Flask(__name__)

    # User authentication, not for production
    app.config['SECRET_KEY'] = 'secret'
    app.config['SIMPLELOGIN_USERNAME'] = 'admin'
    app.config['SIMPLELOGIN_PASSWORD'] = 'password'
    SimpleLogin(app)

    GPIO.setmode(GPIO.BCM)

    # Dictionary to store pin number, name, and state
    pins = {
        10: {'name': 'GPIO 10', 'state': GPIO.LOW},
        11: {'name': 'GPIO 11', 'state': GPIO.LOW},
        12: {'name': 'GPIO 12', 'state': GPIO.LOW},
        13: {'name': 'GPIO 13', 'state': GPIO.LOW},
        14: {'name': 'GPIO 14', 'state': GPIO.LOW},
        15: {'name': 'GPIO 15', 'state': GPIO.LOW},
        16: {'name': 'GPIO 16', 'state': GPIO.LOW},
        17: {'name': 'GPIO 17', 'state': GPIO.LOW},
        18: {'name': 'GPIO 18', 'state': GPIO.LOW},
        19: {'name': 'GPIO 19', 'state': GPIO.LOW},
        20: {'name': 'GPIO 20', 'state': GPIO.LOW},
        21: {'name': 'GPIO 21', 'state': GPIO.LOW},
        22: {'name': 'GPIO 22', 'state': GPIO.LOW},
        23: {'name': 'GPIO 23', 'state': GPIO.LOW},
        24: {'name': 'GPIO 24', 'state': GPIO.LOW},
        25: {'name': 'GPIO 25', 'state': GPIO.LOW},
    }

    # Set each pin as an output and low pull
    for pin in pins:
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, GPIO.LOW)

    # Default route with login required
    @app.route('/')
    @login_required
    def main():
        # Read each pin state and store it
        for pin in pins:
            pins[pin]['state'] = GPIO.input(pin)
        # Copy the pin dictionary into another dictionary to be passed to the template
        template_data = {
            'pins': pins
        }
        # Pass the data into the template
        return render_template('main.html', **template_data)

    # Executed when a request is made to change a pin state
    @app.route("/<current_pin>/<state>")
    @login_required
    def action(current_pin, state):
        # Convert the pin from the URL into an integer and get GPIO pin number
        current_pin = int(current_pin)
        pin_name = pins[current_pin]['name']

        # Toggle the state of the cu
        if state == "on":
            GPIO.output(current_pin, GPIO.HIGH)
            message = "Turned " + pin_name + " on."
        if state == "off":
            GPIO.output(current_pin, GPIO.LOW)
            message = "Turned " + pin_name + " off."

        # Read the pin state and store it
        for pin in pins:
            pins[pin]['state'] = GPIO.input(pin)

        # Copy the pin dictionary into another dictionary to be passed to the template
        template_data = {
            'pins': pins
        }

        return render_template('main.html', **template_data)

    return app


if __name__ == '__main__':
    flask_app = create_app()
    flask_app.run(host='0.0.0.0', port=5000, debug=True)
