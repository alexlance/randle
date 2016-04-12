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

Randle looks for scripts in two directories: *server-todo* and *server-done*.
The latter contains scripts, that check that the former's scripts have executed.

A command like this will connect to three servers and provision them with the
scripts in the *server-todo* directory:

> python -m randle -u USERNAME -p PASSWORD -a 192.168.1.7 -a 192.168.1.8 -a 192.168.1.9

And take a quick look at the options:

> python -m randle --help

Note: if you run *python setup.py install --user* it will build a standalone
randle binary in ~/.local/bin/.


### More info...

The folders *server-todo* and *server-done*, contain scripts that execute on
the server you are provisioning. There must be a parity between the files in
these two directories.

*server-todo* contains scripts that actually do tasks on the server, and
*server-done* should contain scripts to determine if those tasks have been
done.

This is meant to provide a sort of low-tech idempotency. Ie you can run randle
multiple times and no harm done. Eg:

> *server-todo/004-update-config.sh* (performs a tasks)
> #!/bin/bash
> set -e
> echo "some config option" > /etc/config.something

> *server-done/004-update-config.sh* (check that the task was performed)
> #!/bin/bash
> set -e
> # grep exits 1 if pattern not found
> grep "some config option" /etc/config.something 

It is strongly recommended that every script be run using *set -e* so that any
failures anywhere in the script will cause the script to *exit 1* immediately.

The scripts in *server-done* must *exit 1* if you want the sibling task to
execute.


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

