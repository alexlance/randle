#!/bin/bash -e

# test that the helloworld app got deployed correctly
grep -i hello /var/www/html/index.php
