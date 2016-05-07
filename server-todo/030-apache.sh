#!/bin/bash

# ensure our new default.conf got placed in
grep '# Hello World' /etc/apache2/sites-enabled/000-default.conf || run=1

# check apache is running
pidof apache2 || run=1


# setup a quick apache config and start apache
if [ "${run}" ]; then
  rm -f /etc/apache2/sites-enabled/*
  cat << EOF > /etc/apache2/sites-enabled/000-default.conf
  <VirtualHost *:80>
    # Hello World
    DocumentRoot /var/www/html
    ErrorLog \${APACHE_LOG_DIR}/error.log
    CustomLog \${APACHE_LOG_DIR}/access.log combined
  </VirtualHost>
EOF

  # stop apache...
  service apache2 stop

  # kill all processes on port 80 (because Slack was running a netcat process bound to 80)
  processes="$(lsof -t -i:80)"
  [ -n "$processes" ] && kill $processes

  service apache2 start
fi
