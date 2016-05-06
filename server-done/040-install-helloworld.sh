#!/bin/bash
set -e

# test that the helloworld app got deployed correctly
grep -i hello /var/www/html/index.php

# check that the webserver is serving out the app
grep 'Hello, world!' <<<$(curl http://localhost)
