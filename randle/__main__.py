#!/usr/bin/python

""" randle, server configuration tool """

import argparse
import sys
import os
from multiprocessing import Process
from randle.message import Message
from randle.auth import Auth
from randle.server import Server


def get_options():
    """ Setup the command line arguments. """
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('PATH_TO_DEPLOY', type=str, nargs='?', default=".",
                        help='The directory containing the deploy folders (default: pwd)')
    parser.add_argument('-a', dest='ipaddr', action='append', required=True,
                        help='Server to be provisioned (flag can be used multiple times)')
    parser.add_argument('-u', dest='username', required=True,
                        help='ssh login username')
    parser.add_argument('-p', dest='password', required=True,
                        help='ssh login password')
    parser.add_argument('-k', dest='keyfile',
                        help='ssh login private key file (not implemented yet)')
    parser.add_argument('--check', action="store_true",
                        help='Re-verify successful provisioning using server-done/ scripts')
    parser.add_argument('-v', dest='verbose', action="store_true",
                        help='Show verbose output from provisioning')
    return parser.parse_args()


def check_config(p, path):
    """ Ensure that the server-todo and the server-done directories have similarly named files in them. """
    for d in ['server-todo', 'server-done']:
        if not os.path.isdir(os.path.join(path, d)):
            p.err('Missing directory: {}'.format(d))
            sys.exit(1)

    for f in sorted(os.listdir(os.path.join(path, 'server-todo'))):
        if not os.path.isfile(os.path.join(path, 'server-done', f)):
            p.err('File not found: {}'.format(os.path.join(path, 'server-done', f)))
            sys.exit(1)

    for f in sorted(os.listdir(os.path.join(path, 'server-done'))):
        if not os.path.isfile(os.path.join(path, 'server-todo', f)):
            p.err('File not found: {}'.format(os.path.join(path, 'server-todo', f)))
            sys.exit(1)


def provision_server(p, server, options, auth):
    """ Connect to a server and run scripts on it to provision it. """
    s = Server(server, auth)
    s.connect()
    if s.conn_status == s.CONN_OPEN:
        p.msg(' {} {:16s} Connected'.format(p.green('*'), s.host))
    elif s.conn_status == s.CONN_FAILED:
        p.die(' {} {:16s} Authentication failed'.format(p.red('*'), s.host))

    tasks = sorted(os.listdir(os.path.join(options.PATH_TO_DEPLOY, 'server-todo')))
    for t in tasks:
        done_exit, done_output, done_errors = s.execute_task(os.path.join(options.PATH_TO_DEPLOY, 'server-done', t))
        if done_exit:
            p.warn('   {:16s} {:22s} {}'.format(s.host, t, p.orange('skipped')))
        else:
            todo_exit, todo_output, todo_errors = s.execute_task(os.path.join(options.PATH_TO_DEPLOY, 'server-todo', t))
            if todo_exit:
                p.msg('   {:16s} {:22s} {}'.format(s.host, t, p.green('done')))
            else:
                p.err('   {:16s} {:22s} {}'.format(s.host, t, p.red('error: '+str(todo_errors).rstrip())))

            if options.check:
                done_exit, done_output, done_errors = s.execute_task(os.path.join(options.PATH_TO_DEPLOY, 'server-done', t))
                if not done_exit:
                    p.warn('   {:16s} {:22s} warning: {} does not indicate success.'
                           .format(s.host, t, os.path.join(options.PATH_TO_DEPLOY, 'server-done', t)))

            if options.verbose:
                if todo_output:
                    p.msg('   {}: {:22s} output: {}'.format(s.host, t, str(todo_output).rstrip()))

    s.disconnect()


def main():
    """ Run a bunch of scripts on a bunch of servers. """
    p = Message()
    options = get_options()
    check_config(p, options.PATH_TO_DEPLOY)

    auth = Auth()
    auth.set_username(options.username)
    auth.set_password(options.password)

    processes = []
    for server in options.ipaddr:
        proc = Process(target=provision_server, args=(p, server, options, auth))
        proc.start()
        processes.append(proc)

    for proc in processes:
        proc.join()


if __name__ == "__main__":
    main()
