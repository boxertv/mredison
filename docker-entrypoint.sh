#!/bin/bash

## Mount needed for GPIO pins to be enabled correctly
mount -t debugfs nodev /sys/kernel/debug && \
sleep 5 && \
python /mredison/mredison.py
