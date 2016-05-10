#!/bin/bash
#
# Test that the helloworld app got deployed correctly into apache's document
# root and that the application is being served correctly. If not, git clone it
# into the web root.

grep -i hello /var/www/html/index.php || run=1

# check that the webserver is serving out the app
grep 'Hello, world!' <<<$(curl -s http://localhost) || run=1

# checkout the helloworld application into apache's DocumentRoot
if [ "${run}" ]; then
  echo "Checking out source for helloworld" > /dev/stderr
  rm -rf /var/www/html
  git clone https://github.com/alexlance/helloworld /var/www/html
  chmod -R a+r /var/www/html
fi
