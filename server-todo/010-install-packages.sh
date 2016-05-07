#!/bin/bash

is_installed() {
  dpkg-query -Wf'${db:Status-abbrev}' "$1" 2>/dev/null | grep -q '^i'
}

purge_and_install() {
  apt-get purge -y $1
  apt-get -o Dpkg::Options::="--force-confmiss" install --reinstall -y $1
}

deps="ufw apache2-mpm-prefork php5 git"

for i in $deps; do
  is_installed $i || purge_and_install $i
done

