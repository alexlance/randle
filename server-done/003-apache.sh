#!/bin/bash -e

# ensure our new default.conf got placed in
grep 'DocumentRoot /var/www/html' /etc/apache2/sites-enabled/000-default.conf

