# Randle - server configuration tool

*(named after Randle McMurphy - because this approach miight be slightly deranged)*


### Synopsis

Given a pool of servers, and a bunch of provisioning shell scripts, randle
opens an ssh connection to each server and runs the scripts.


### Features

* Multiple servers can be provisioned simultaneously

* Un-opinionated provisioning - they're your provisioning scripts

* Idempotent, only performs the provisioning tasks that need to be done


### Quick start

A command like this will connect to three servers and provision them with the
scripts in the directory you specify:

> python -m randle -d server-todo/ -u USERNAME -p PASSWORD -a 192.168.1.7 -a 192.168.1.8 -a 192.168.1.9 

And take a quick look at the options:

> python -m randle --help

Note: if you run *python setup.py install --user* it will build a standalone
randle binary in ~/.local/bin/.


### More info...

The -d argument lets you specify a folder that contains provisioning scripts
that you want to execute on a server. It is up to you to make your scripts
idempotent. Ensure your scripts exit with a non-zero status if they fail.

> *server-todo/004-update-config.sh*
> #!/bin/bash
>
> grep "some config option" /etc/config.something || run=1
>
> if [ "${run}" ]; then
>   echo "Missing the config option! Writing it now..." > /dev/stderr
>   echo "some config option" > /etc/config.something
> fi

Note that by echoing some info to stderr, this tool interprets that as a
message that the user should see.


### Ideas for the future

* Interrogate a load balancer to dynamically determine the instances beneath it
  that require provisioning

* Support for pre-hook operations and post-hook operations (for deploy
  strategies)

* Or built-in deployment strategies, rolling, blue-green, red-black, canary
  deployment?

* Scripts are not OS agnostic. Ie, apt vs yum etc. But the OS agnostic
  abstraction can be pretty leaky.

* Only does IP addresses at the moment (doesn't resolve hostnames)

* The pre-hook could provision a brand new server(s) and could theoretically
  return the IP address to the main randle process in some fashion, so that the
  new server can be provisioned (for eg red-black deploys)

* Add support for privilege escalation, and ssh keys for auth


### Dependencies

* Python 2.7.9 (it may Just Work on other versions too)

* Python Paramiko (I'm using python-paramiko/stable,now 1.15.1-1 on debian:jessie)

