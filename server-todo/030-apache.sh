#!/bin/bash
set -e

# setup a quick apache config
rm -f /etc/apache2/sites-enabled/* || true
cat << EOF > /etc/apache2/sites-enabled/000-default.conf
<VirtualHost *:80>
  # Hello World
  DocumentRoot /var/www/html
  ErrorLog \${APACHE_LOG_DIR}/error.log
  CustomLog \${APACHE_LOG_DIR}/access.log combined
</VirtualHost>
EOF

# stop apache...
service apache2 stop || true

# kill all processes on port 80 (because Slack was running a netcat process bound to 80)
processes="$(lsof -t -i:80 || true)"
[ -n "$processes" ] && kill $processes

service apache2 start

