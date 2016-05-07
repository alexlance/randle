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
    parser.add_argument('-d', dest='directory', required=True,
                        help='The directory containing the provisioning scripts')
    parser.add_argument('-a', dest='ipaddr', action='append', required=True,
                        help='Server to be provisioned (flag can be used multiple times)')
    parser.add_argument('-u', dest='username', required=True,
                        help='ssh login username')
    parser.add_argument('-p', dest='password', required=True,
                        help='ssh login password')
    parser.add_argument('-k', dest='keyfile',
                        help='ssh login private key file (not implemented yet)')
    parser.add_argument('-v', dest='verbose', action="store_true",
                        help='Show verbose output from provisioning')
    parser.add_argument('-q', dest='quiet', action="store_true",
                        help='Show much less output, only errors')
    return parser.parse_args()


def provision_server(p, server, options, auth):
    """ Connect to a server and run scripts on it to provision it. """
    s = Server(server, auth)
    s.connect()

    if s.connection_open():
        p.msg(' {} {:16s} Connected'.format(p.green('*'), s.host))
    elif s.connection_failed():
        p.die(' {} {:16s} Authentication failed'.format(p.red('*'), s.host))

    tasks = sorted(os.listdir(os.path.join(options.directory)))
    for t in tasks:
        p.msg('   {:16s} {:30s} {}'.format(s.host, t, p.orange('executing')))
        result, output, errors = s.execute_task(os.path.join(options.directory, t))

        if options.verbose:
            p.msg(' {} {:16s} {:30s} verbose: {}'.format(p.orange('*'), s.host, t, output))

        # If a script writes to stderr but exits 0, the we interpret that as a message to be seen
        if result and errors:
            p.err('   {:16s} {:30s} {}'.format(s.host, t, p.orange(errors)))

        elif not result:
            p.err('   {:16s} {:30s} {}'.format(s.host, t, p.red(errors)))
            s.disconnect()
            p.msg(' {} {:16s} Disconnected'.format(p.green('*'), s.host))
            return
    p.msg(' {} {:16s} Disconnected'.format(p.green('*'), s.host))
    s.disconnect()


def main():
    """ Run a bunch of scripts on a bunch of servers. """
    options = get_options()
    p = Message(options.quiet)

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
