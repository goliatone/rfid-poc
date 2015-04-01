#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import argparse
import traceback
import time
import httplib
import requests
import json
import ConfigParser
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

KEY_ENTER = 'KEY_ENTER'
DEVICE_NAME = 'RFIDeas USB Keyboard'

URI = None
HOST = None
URL_TEMPLATE = None
UUID = None

ON_RFID = None


def get_default_payload(rfid):
    return {'uuid': UUID, 'rfid': rfid}


def make_request(rfid):
    payload = get_default_payload(rfid)

    command = 'on' if (rfid == ON_RFID) else 'off'

    url = URL_TEMPLATE % (HOST, URI, command)
    headers = {'content-type': 'application/json'}

    try:
        requests.post(url, data=json.dumps(payload), headers=headers)
    except Exception as e:
        print 'Error: ', e



def get_scanner_device():
    devices = map(InputDevice, list_devices())
    device = None
    for dev in devices:
        if dev.name == DEVICE_NAME:
            device = dev
            break
    return device


def read_input(device):
    rfid = ''
    for event in device.read_loop():
        data = categorize(event)
        if event.type == ecodes.EV_KEY and data.keystate == data.key_down:
            if data.keycode == KEY_ENTER:
                break
            rfid += SCANCODES[data.scancode]
    return rfid


def init(dev):
    if str(dev) == 'None':
        print "Device not found"
        sys.exit(1)

    try:
        device = InputDevice(dev.fn)
        device.grab()
    except:
        print "Unable to grab input device"
        sys.exit(1)

    return device


def cleanup(device):
    device.ungrab()


def configure(path='config.ini'):
    config = ConfigParser.ConfigParser()
    config.read(path)

    URI = config.get('requests', 'uri')
    HOST = config.get('requests', 'host')
    URL_TEMPLATE = config.get('requests', 'url_template')

    UUID = config.get('auth', 'uuid')

    print "Initialize %s" %UUID


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='RFID demo')
    parser.add_argument('-o', '--on', required=True, help='RFID associated with on command')
    args = parser.parse_args()

    ON_RFID = args.on

    config_path = args.config
    configure(path=config_path)

    device_name = get_scanner_device()
    device = init(device_name)

    print "Found device: %s" % DEVICE_NAME

    while True:
        try:
            rfid = read_input(device)
            make_request(rfid)
            print "RFID card read, value: %s" %rfid
        except ValueError:
            time.sleep(0.1)
        except Exception, e:
            print e
            cleanup(device)
            sys.exit(1)
