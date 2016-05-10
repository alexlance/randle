#!/bin/bash
#
# Check that there's more than 20mb of diskspace free on the root filesystem.
# If not, print an error to /dev/stderr and exit 1.

[ "$(df --output=avail / | tail -n +2)" -gt 20000 ] || run=1

if [ "${run}" ]; then
  echo "Not enough diskspace. Exiting." > /dev/stderr
  exit 1
fi
