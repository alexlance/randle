#!/bin/bash
set -e

# install packages
apt-get update
apt-get purge -y ufw php5 git apache2 apache2-mpm-prefork
rm -rf /etc/ufw /lib/ufw /etc/apache2 /etc/php5 # it'd be nice if apt-get would purge correctly
apt-get -o Dpkg::Options::="--force-confmiss" install --reinstall -y ufw php5 git apache2-mpm-prefork

