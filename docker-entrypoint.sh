#!/bin/bash

if mount -l -t debugfs | grep "on /sys/kernel/debug"; then
    echo "debugfs already mounted"
else
    mount -t debugfs nodev /sys/kernel/debug
fi

udevadm trigger

python /mredison/mredison.py
