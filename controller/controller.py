# import the required modules
import time
import RPi.GPIO as GPIO


SWITCH_1 = 11
SWITCH_2 = 15
SWITCH_3 = 16
SWITCH_4 = 13

ON = ['1011', '1111', '1110', '1101', '1100']
OFF = ['0011', '0111', '0110', '0101', '0100']


class SwitchController(object):
    def __init__(self):
        # set the pins numbering mode
        GPIO.setmode(GPIO.BOARD)

        # Select the GPIO pins used for the encoder K0-K3 data inputs
        GPIO.setup(SWITCH_1, GPIO.OUT)
        GPIO.setup(SWITCH_2, GPIO.OUT)
        GPIO.setup(SWITCH_3, GPIO.OUT)
        GPIO.setup(SWITCH_4, GPIO.OUT)

        # Select the signal to select ASK/FSK
        GPIO.setup(18, GPIO.OUT)

        # Select the signal used to enable/disable the modulator
        GPIO.setup(22, GPIO.OUT)

        # Disable the modulator by setting CE pin lo
        GPIO.output(22, False)

        # Set the modulator to ASK for On Off Keying
        # by setting MODSEL pin lo
        GPIO.output(18, False)

        # Initialise K0-K3 inputs of the encoder to 0000
        GPIO.output(11, False)
        GPIO.output(15, False)
        GPIO.output(16, False)
        GPIO.output(13, False)

        try:
            # We will just loop round switching the units on and off
            while True:
                raw_input('hit return key to send socket 1 ON code')
                # Set K0-K3
                print "sending code 1111 socket 1 on"
                GPIO.output(11, True)
                GPIO.output(15, True)
                GPIO.output(16, True)
                GPIO.output(13, True)
                # let it settle, encoder requires this
                time.sleep(0.1)
                # Enable the modulator
                GPIO.output(22, True)
                # keep enabled for a period
                time.sleep(0.25)
                # Disable the modulator
                GPIO.output(22, False)

                raw_input('hit return key to send socket 1 OFF code')
                # Set K0-K3
                print "sending code 0111 Socket 1 off"
                GPIO.output(11, True)
                GPIO.output(15, True)
                GPIO.output(16, True)
                GPIO.output(13, False)
                # let it settle, encoder requires this
                time.sleep(0.1)
                # Enable the modulator
                GPIO.output(22, True)
                # keep enabled for a period
                time.sleep(0.25)
                # Disable the modulator
                GPIO.output(22, False)

                raw_input('hit return key to send socket 2 ON code')
                # Set K0-K3
                print "sending code 1110 socket 2 on"
                GPIO.output(11, False)
                GPIO.output(15, True)
                GPIO.output(16, True)
                GPIO.output(13, True)
                # let it settle, encoder requires this
                time.sleep(0.1)
                # Enable the modulator
                GPIO.output(22, True)
                # keep enabled for a period
                time.sleep(0.25)
                # Disable the modulator
                GPIO.output(22, False)

                raw_input('hit return key to send socket 2 OFF code')
                # Set K0-K3
                print "sending code 0110 socket 2 off"
                GPIO.output(11, False)
                GPIO.output(15, True)
                GPIO.output(16, True)
                GPIO.output(13, False)
                # let it settle, encoder requires this
                time.sleep(0.1)
                # Enable the modulator
                GPIO.output(22, True)
                # keep enabled for a period
                time.sleep(0.25)
                # Disable the modulator
                GPIO.output(22, False)

                raw_input('hit return key to send ALL ON code')
                # Set K0-K3
                print "sending code 1011 ALL on"
                GPIO.output(11, True)
                GPIO.output(15, True)
                GPIO.output(16, False)
                GPIO.output(13, True)
                # let it settle, encoder requires this
                time.sleep(0.1)
                # Enable the modulator
                GPIO.output(22, True)
                # keep enabled for a period
                time.sleep(0.25)
                # Disable the modulator
                GPIO.output(22, False)

                raw_input('hit return key to send ALL OFF code')
                # Set K0-K3
                print "sending code 0011 All off"
                GPIO.output(11, True)
                GPIO.output(15, True)
                GPIO.output(16, False)
                GPIO.output(13, False)
                # let it settle, encoder requires this
                time.sleep(0.1)
                # Enable the modulator
                GPIO.output(22, True)
                # keep enabled for a period
                time.sleep(0.25)
                # Disable the modulator
                GPIO.output(22, False)

        # Clean up the GPIOs for next time
        except KeyboardInterrupt:
            GPIO.cleanup()

        def change_plug_state(socket, on_or_off):
            state = on_or_off[socket][3] == '1'
            GPIO.output(SWITCH_1, state)
            state = on_or_off[socket][2] == '1'
            GPIO.output(SWITCH_2, state)
            state = on_or_off[socket][1] == '1'
            GPIO.output(SWITCH_3, state)
            state = on_or_off[socket][0] == '1'
            GPIO.output(SWITCH_4, state)
            sleep(0.1)
            GPIO.output(ENABLE, True)
            sleep(0.25)
            GPIO.output(ENABLE, False)

        def switch_on(socket):
            change_plug_state(socket, ON)

        def switch_off(socket):
            change_plug_state(socket, OFF)
