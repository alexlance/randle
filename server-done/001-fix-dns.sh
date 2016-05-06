#!/bin/bash
set -e

# test the namesservers in resolv.conf
for server in $(awk '$1 == "nameserver" { print $2 }' /etc/resolv.conf); do
  dig +short google.com in ns @${server}
done
