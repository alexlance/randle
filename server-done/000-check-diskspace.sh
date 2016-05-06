#!/bin/bash
set -e

# probably going to be issues if there's less than 20mb free on the root filesystem
[ "$(df --output=avail / | grep -vi avail)" -gt 20000 ]
