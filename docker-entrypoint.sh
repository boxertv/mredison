#!/bin/bash

# Based on: http://talk.resin.io/t/libusb0-py-cannot-open-a-directory/62/16

# Mount needed for GPIO pins to be enabled correctly
if mount -l -t debugfs | grep "on /sys/kernel/debug"; then
    echo "debugfs already mounted"
else
    mount -t debugfs nodev /sys/kernel/debug
fi

udevd & udevadm trigger

python /mredison/mredison.py
