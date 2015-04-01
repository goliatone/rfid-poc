
## Description

This is a sample script reading the input from an USB RFID reader connected to a Raspberry Pi to trigger on/off commands controlling a LED light bulb.

The RFID used is a [RFIDeas pcProx 125 kHz][rfid] which basically simulates keyboard input.

The python script uses [evdev][evdev] to read the input and make a POST request to a controller server that manages the light bulbs.


## Documentation

Once you plug the RFID reader to the Pi's USB, if you run the `lsusb` command it should be listed there:

```
Bus 001 Device 002: ID 0424:9514 Standard Microsystems Corp. 
Bus 001 Device 001: ID 1d6b:0002 Linux Foundation 2.0 root hub
Bus 001 Device 003: ID 0424:ec00 Standard Microsystems Corp. 
Bus 001 Device 004: ID 0bda:8176 Realtek Semiconductor Corp. RTL8188CUS 802.11n WLAN Adapter
Bus 001 Device 005: ID 0c27:3bfa RFIDeas, Inc pcProx Card Reader
```

Once your device is recognized, you can run the script:

```bash
$ sudo python rfid_light.py -o 2714
```

The **-o** option is the RFID card number that will be used to trigger the **on** command. Any other value will trigger the **off** command. Simple as that.


## Config

```ini
[auth]
uuid: '3444d6844dd36514dd44411455cfb596'
token: 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9'

[requests]
uri = '/command/'
host = 'myserver.com'
url_template = 'http://%s%s%s'
```


[rfid]: https://www.rfideas.com/support/product-support/pcprox-125-khz-enroll
[evdev]: https://github.com/gvalkov/python-evdev