#!/bin/bash
set -e

# firewall only allow 80 and 22
yes | ufw reset
ufw allow ssh/tcp
ufw allow http/tcp
yes | ufw enable
