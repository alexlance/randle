#!/bin/bash

# test that the helloworld app got deployed correctly
grep -i hello /var/www/html/index.php || run=1

# check that the webserver is serving out the app
grep 'Hello, world!' <<<$(curl http://localhost) || run=1

# checkout the helloworld application into apache's DocumentRoot
if [ "${run}" ]; then
  rm -rf /var/www/html
  git clone https://github.com/alexlance/helloworld /var/www/html
  chmod -R a+r /var/www/html
fi
