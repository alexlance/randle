#!/bin/bash

# probably going to be issues if there's less than 20mb free on the root filesystem
[ "$(df --output=avail / | grep -vi avail)" -gt 20000 ]

if [ "$?" -ne 0 ]; then
  echo "Not enough diskspace. Exiting." > /dev/stderr
  exit 1
fi
