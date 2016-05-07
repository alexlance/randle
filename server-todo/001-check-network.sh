#!/bin/bash

ping -c 1 google.com

if [ "$?" -ne 0 ]; then
  echo "Cannot ping google. Exiting." > /dev/stderr
  exit 1
fi
