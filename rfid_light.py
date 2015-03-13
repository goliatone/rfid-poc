#!/usr/bin/python

import sys
import time
from evdev import InputDevice, list_devices, categorize, ecodes

SCANCODES = {
    # Scancode: ASCIICode
    0: None, 1: u'ESC', 2: u'1', 3: u'2', 4: u'3', 5: u'4', 6: u'5', 7: u'6', 8: u'7', 9: u'8',
    10: u'9', 11: u'0', 12: u'-', 13: u'=', 14: u'BKSP', 15: u'TAB', 16: u'Q', 17: u'W', 18: u'E', 19: u'R',
    20: u'T', 21: u'Y', 22: u'U', 23: u'I', 24: u'O', 25: u'P', 26: u'[', 27: u']', 28: u'CRLF', 29: u'LCTRL',
    30: u'A', 31: u'S', 32: u'D', 33: u'F', 34: u'G', 35: u'H', 36: u'J', 37: u'K', 38: u'L', 39: u';',
    40: u'"', 41: u'`', 42: u'LSHFT', 43: u'\\', 44: u'Z', 45: u'X', 46: u'C', 47: u'V', 48: u'B', 49: u'N',
    50: u'M', 51: u',', 52: u'.', 53: u'/', 54: u'RSHFT', 56: u'LALT', 100: u'RALT'
}


def get_scanner_device():
    devices = map(InputDevice, list_devices())
    device = None
    for dev in devices:
        print dev.name
    if dev.name == 'RFIDeas USB Keyboard':
        device = InputDevice(dev.fn)
            break
    return device


def init(device):
    pass


if __name__ == "__main__":
    device = get_scanner_device()
    if str(device) == 'None':
    print "Device not found"
    sys.exit(1)

    try:
    device.grab()
    except:
        print "Unable to grab input device"
    sys.exit(1)

    init(device)

    while True:
    try:
        rfid = ""
        for event in device.read_loop():
        data = categorize(event)
        if event.type == ecodes.EV_KEY and data.keystate == data.key_down:
            if data.keycode == 'KEY_ENTER':
            break
            rfid += SCANCODES[data.scancode]
        print "KEY CODE %s" %rfid
    except ValueError:
        print "ERROR"
        time.sleep(0.1)