#!/bin/sh
### BEGIN INIT INFO
# Provides:          rfid_led
# Required-Start:    $remote_fs $syslog $network
# Required-Stop:     $remote_fs $syslog $network
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# Short-Description: init.d script for rfid_led service
# Description:       rfid_led is an RFID card reader controlling an LED
### END INIT INFO

PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
NAME=rfid_led

APP_ROOT=/home/pi/CODE/rfideas
DAEMON=$APP_ROOT/rfid_led.py

# Add any command line options for your daemon here
DAEMONARGS="-C $APP_ROOT/config.ini -O 2714"

# The process ID of the script when it runs is stored here:
PIDFILE=/var/run/$NAME.pid

# The process log file
LOGFILE=/var/log/$NAME.log

# Define LSB log_* functions.
# Depend on lsb-base (>= 3.2-14) to ensure that this file is present
# and status_of_proc is working.
. /lib/lsb/init-functions

test -f $DAEMON || exit 0

case "$1" in
    start)
        start-stop-daemon --start --background \
            --pidfile $PIDFILE --make-pidfile --startas /bin/bash \
            -- -c "exec stdbuf -oL -eL $DAEMON $DAEMONARGS > $LOGFILE 2>&1"
        log_end_msg $?
        ;;
    stop)
        start-stop-daemon --stop --pidfile $PIDFILE
        log_end_msg $?
        rm -f $PIDFILE
        ;;
    restart)
        $0 stop
        $0 start
        ;;
    status)
        start-stop-daemon --status --pidfile $PIDFILE
        log_end_msg $?
        ;;
    *)
        echo "Usage: $0 {start|stop|restart|status}"
        exit 2
        ;;
esac

exit 0