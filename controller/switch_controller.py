# import the required modules
import time
import RPi.GPIO as GPIO

PIN_1 = 11
PIN_2 = 15
PIN_3 = 16
PIN_4 = 13

ON_OFF_KEY = 18
ENABLE = 22

ON = [
    # All
    [True, False, True, True],
    # 1
    [True, True, True, True],
    # 2
    [True, True, True, False],
    # 3
    [True, True, False, True],
    #4
    [True, True, False, False]
]

OFF = [
    # All
    [False, False, True, True],
    # 1
    [False, True, True, True],
    # 2
    [False, True, True, False],
    # 3
    [False, True, False, True],
    # 4
    [False, True, False, False]
]


class SwitchController(object):
    def __init__(self):
        # set the pins numbering mode
        GPIO.setmode(GPIO.BOARD)

        # Select the GPIO pins used for the encoder K0-K3 data inputs
        GPIO.setup(PIN_1, GPIO.OUT)
        GPIO.setup(PIN_2, GPIO.OUT)
        GPIO.setup(PIN_3, GPIO.OUT)
        GPIO.setup(PIN_4, GPIO.OUT)

        # Select the signal to select ASK/FSK
        GPIO.setup(ON_OFF_KEY, GPIO.OUT)

        # Select the signal used to enable/disable the modulator
        GPIO.setup(ENABLE, GPIO.OUT)

        # Disable the modulator by setting CE pin lo
        GPIO.output(ENABLE, False)

        # Set the modulator to ASK for On Off Keying
        # by setting MODSEL pin lo
        GPIO.output(ON_OFF_KEY, False)

        # Initialise K0-K3 inputs of the encoder to 0000
        GPIO.output(PIN_1, False)
        GPIO.output(PIN_2, False)
        GPIO.output(PIN_3, False)
        GPIO.output(PIN_4, False)

    def change_plug_state(self, pin_states):
        GPIO.output(PIN_4, pin_states[0])
        GPIO.output(PIN_3, pin_states[1])
        GPIO.output(PIN_2, pin_states[2])
        GPIO.output(PIN_1, pin_states[3])
        time.sleep(0.1)
        GPIO.output(ENABLE, True)
        time.sleep(0.25)
        GPIO.output(ENABLE, False)

    def switch_on(self, socket):
        self.change_plug_state(ON[socket])

    def switch_off(self, socket):
        self.change_plug_state(OFF[socket])

    def wait_for_input(self):
        # We will just loop round switching the units on and off
        while True:
            raw_input('hit return key to send socket 1 ON code')
            self.switch_on(1)

            raw_input('hit return key to send socket 1 OFF code')
            self.switch_off(1)

            raw_input('hit return key to send socket 2 ON code')
            self.switch_on(2)

            raw_input('hit return key to send socket 2 OFF code')
            self.switch_off(2)

            raw_input('hit return key to send ALL ON code')
            self.switch_on(0)

            raw_input('hit return key to send ALL OFF code')
            self.switch_off(0)


if __name__ == '__main__':
    try:
        controller = SwitchController()
        controller.wait_for_input()
    except KeyboardInterrupt:
        # Clean up the GPIOs for next time
        GPIO.cleanup()