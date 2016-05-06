#!/bin/bash
set -e

# ensure our new default.conf got placed in
grep '# Hello World' /etc/apache2/sites-enabled/000-default.conf

# check apache is running
pidof apache2
