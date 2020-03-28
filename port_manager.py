import rtmidi

from backend import *
from parameters import *

import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(16,GPIO.OUT)
GPIO.setup(26,GPIO.OUT)

'''
If the input is disconected, the system enters "scanmode" where it looks

'''

class PortManager:
    def __init__(self, pref_device=SUPPORTED_DEVICES[0]):
        self.input_name = None
        self.preferred_device = pref_device
        self._availables = None
        self.midi_instance = rtmidi.MidiIn()
        self.scanner_daemon = DaemonRoutine(ROUTINE_DELAY, self._check_available_devices, t_name="Scanner daemon")
        self.is_scanning = True

    def _get_avail_set(self):
        return set(self.midi_instance.get_ports()) & set(SUPPORTED_DEVICES)

    def _check_available_devices(self):
        if self._availables != self._get_avail_set():
            if self.input_name not in self._get_avail_set():
                self.input_name = None
                self._scanmode()
            self._availables = self._get_avail_set()

        return self._availables

    def _scanmode(self):
        self.is_scanning = True
        GPIO.output(26, GPIO.HIGH)
        GPIO.output(16, GPIO.LOW)
        print("\n\n\rScanning for devices...", end="")
        scan = self._get_avail_set()
        if bool(scan):
            if self.preferred_device in scan:
                self.input_name = self.preferred_device
            else:
                self.input_name = scan[0]
            print("\rFOUND DEVICE NAME: %s"%self.input_name)
            self.is_scanning = False
            GPIO.output(26, GPIO.LOW)
            GPIO.output(16, GPIO.HIGH)









