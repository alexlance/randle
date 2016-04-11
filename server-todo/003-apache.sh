#!/bin/bash
set -e

# setup a quick apache config
rm -f /etc/apache2/sites-enabled/*
cat << EOF > /etc/apache2/sites-enabled/000-default.conf
<VirtualHost *:80>
  # Hello World
  DocumentRoot /var/www/html
  ErrorLog ${APACHE_LOG_DIR}/error.log
  CustomLog ${APACHE_LOG_DIR}/access.log combined
</VirtualHost>
EOF

# restart apache...
# systemd is in 15.04, but the boxes slack have provided are running 14.04
# doesn't work: systemctl restart apache2
# doesn't work: restart apache2
/etc/init.d/apache2 restart


