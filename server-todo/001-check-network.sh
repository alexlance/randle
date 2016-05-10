#!/bin/bash
#
# Attempt to ping a known host that works, if we can't reach it then print an
# error to /dev/stderr and exit 1.

ping -c 1 google.com || run=1

if [ "${run}" ]; then
  echo "Cannot ping google. Exiting." > /dev/stderr
  exit 1
fi
