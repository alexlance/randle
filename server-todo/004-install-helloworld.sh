#!/bin/bash
set -e

# checkout the helloworld application into apache's DocumentRoot
rm -rf /var/www/html
git clone https://github.com/alexlance/helloworld /var/www/html
chmod -R a+r /var/www/html
