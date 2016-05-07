#!/bin/bash

# check that the firewall has been setup correctly
ufw status verbose | grep -E 'Status: active'      || run=1
ufw status verbose | grep -E '22.*ALLOW.*Anywhere' || run=1
ufw status verbose | grep -E '80.*ALLOW.*Anywhere' || run=1

# default settings ok (this is a bit fragile, fix me)
ufw status verbose | grep 'Default: deny (incoming), allow (outgoing), disabled (routed)' || run=1

# check there are only two rules
[ "$(ufw status | grep ALLOW | grep -v v6 | wc -l)" == 2 ] || run=1

# firewall: only allow ports 80 and 22
if [ "${run}" ]; then
  echo "Fixing firewall" > /dev/stderr
  yes | ufw reset
  ufw allow ssh/tcp
  ufw allow http/tcp
  yes | ufw enable
fi
