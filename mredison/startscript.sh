#!/usr/bin/bash

mount -t debugfs nodev /sys/kernel/debug && \
python ./mredison.py
