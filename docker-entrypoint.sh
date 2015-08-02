#!/bin/bash

## Mount needed for GPIO pins to be enabled correctly
mount -t debugfs nodev /sys/kernel/debug && \
python /mredison/mredison.py
