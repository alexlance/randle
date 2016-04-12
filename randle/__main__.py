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
    parser.add_argument('DIR', type=str, nargs='?', default=".",
                        help='The directory containing server-todo and server-done folders (default: pwd)')
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
    parser.add_argument('-q', dest='quiet', action="store_true",
                        help='Show much less output, only errors')
    parser.add_argument('-f', dest='force', action="store_true",
                        help='Force provisioning regardless of what server-done/ says')
    return parser.parse_args()


def check_config(p, path, options):
    """ Ensure that the server-todo and the server-done directories have similarly named files in them. """
    for d in ['server-todo', 'server-done']:
        if not os.path.isdir(os.path.join(path, d)):
            p.err('Missing directory: {}'.format(d))
            sys.exit(1)

    for f in sorted(os.listdir(os.path.join(path, 'server-todo'))):
        if not os.path.isfile(os.path.join(path, 'server-done', f)) and not options.force:
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

    tasks = sorted(os.listdir(os.path.join(options.DIR, 'server-todo')))
    for t in tasks:
        done_good, done_output, done_errors = s.execute_task(os.path.join(options.DIR, 'server-done', t))
        if done_good and not options.force:
            p.warn('   {:16s} {:30s} {}'.format(s.host, t, p.orange('skipped')))
            if options.verbose:
                p.msg(' {} {:16s} {:30s} verbose done: {}'.format(p.orange('*'), s.host, t, str(done_output).rstrip()))

        else:
            todo_good, todo_output, todo_errors = s.execute_task(os.path.join(options.DIR, 'server-todo', t))
            if todo_good:
                p.msg('   {:16s} {:30s} {}'.format(s.host, t, p.green('done')))
            else:
                p.err('   {:16s} {:30s} {}'.format(s.host, t, p.red('error: '+str(todo_errors).rstrip())))

            if options.verbose:
                p.msg(' {} {:16s} {:30s} verbose todo: {}'.format(p.orange('*'), s.host, t, str(todo_output).rstrip()))

            if options.check:
                done_good2, done_output2, done_errors2 = s.execute_task(os.path.join(options.DIR, 'server-done', t))
                if not done_good2:
                    p.warn('   {:16s} {:30s} warning: {} does not indicate success.'
                           .format(s.host, t, os.path.join(options.DIR, 'server-done', t)))
                if options.verbose:
                    p.msg(' {} {:16s} {:30s} verbose check: {}'.format(p.orange('*'), s.host, t, str(done_output2).rstrip()))

    s.disconnect()


def main():
    """ Run a bunch of scripts on a bunch of servers. """
    options = get_options()
    p = Message(options.quiet)
    check_config(p, options.DIR, options)

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
