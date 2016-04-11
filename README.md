# Randle - server configuration tool

*(named after Randle McMurphy - because this approach is a teeny bit braindead)*


### Synopsis

Given a pool of servers, and a bunch of shell scripts that you want to run on them,
randle opens ssh connections to each server and runs the scripts.


### Features

* Multiple servers can be provisioned at a time.

* Support for pre-hook operations and post-hook operations (for deploy
  strategies)

* Un-opinionated provisioning - they're your provisioning scripts


### Directory layout

Scripts that are in the *pre-hook* and *post-hook* directories are run
**locally** on the machine that you have executed Randle on. 

> Eg:
> a script in the *pre-hook* folder might take a server instance out of the
> load balancer before provisioning. And a script in *post-hook* could perform
> tests on the newly provisioned instance (to ensure it is healthy) and if
> healthy, place it back under the load balancer.

The folders *server-todo* and *server-done*, contain scripts that execute
**on the server** you are provisioning. *server-todo* actually does stuff
on the server, and *server-done* should contain scripts to determine *if*
that stuff has been done. All scripts must exit non-zero on failure.

> Eg:  
> *server-todo/004-packages.sh* (installs some packages)
> *server-done/004-packages.sh* (check whether those packages have been installed)

This is meant to provide a sort of low-tech idempotency. Ie you can run it
multiple times and no harm done.


### Quick start

First create a folder structure somewhere:

> mkdir -p ./randle_dirs/{pre-hook,post-hook,server-todo,server-done}

And populate the server-todo folder with scripts that you'd like to run on the
servers you are provisioning. The scripts will be executed in regular directory
order. So it makes sense to name them eg: *001-do-stuff.sh, 002-do-other-things.sh*.


Eg: a command like this will connect to three servers and provision them:

> main.py -u USERNAME -p PASSWORD -a 192.168.1.7 -a 192.168.1.8 -a 192.168.9 ./randle_dirs/

Each script inside *server-todo* should have a corresponding sibling script in *server-done*
with the same filename. The scripts in server-done can just exit 0 if they're not needed. Or exit 1
if you want the sibling to *always* execute.


### Ideas for the future

* Should be able to interrogate a load balancer to dynamically determine the
  instances beneath it that require provisioning?

* Built-in deployment strategies, rolling, blue-green, red-black, canary deployment?

* Scripts are not OS agnostic. Ie, apt vs yum etc. But I'm ok with that. The OS
  agnostic abstraction can be pretty leaky anyway.

* Only does IP addresses at the moment (doesn't resolve hostnames)

* The pre-hook could provision a brand new server(s) and could theoretically
  return the IP address to the main randle process in some fashion, so that the
  new server can be provisioned (for eg red-black deploys)


### Dependencies

* needs python paramiko

