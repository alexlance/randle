#!/bin/bash -e

# check that the firewall has been setup correctly
ufw status verbose | grep -E 'Status: active'
ufw status verbose | grep -E '22.*ALLOW.*Anywhere'
ufw status verbose | grep -E '80.*ALLOW.*Anywhere'
ufw status verbose | grep -E 'Default: deny (incoming), allow (outgoing), disabled (routed)' # fragile, FIXME

# check there are only two rules
[ "$(ufw status | grep ALLOW | grep -v v6 | wc -l)" == 2 ] || exit 1
