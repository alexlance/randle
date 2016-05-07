""" randle, server configuration tool """

import argparse
import os
from multiprocessing import Process
from randle.message import Message
from randle.auth import Auth
from randle.server import Server


def get_options():
    """ Setup the command line arguments. """
    parser = argparse.ArgumentParser(prog='randle', description='Provision servers \
                                     using a directory containing shell scripts')
    parser.add_argument('-d', dest='directory', required=True,
                        help='directory containing the provisioning scripts')
    parser.add_argument('-a', dest='ipaddr', action='append', required=True,
                        help='servers to be provisioned (use -a multiple times)')
    parser.add_argument('-u', dest='username', required=True,
                        help='ssh username')
    parser.add_argument('-p', dest='password', required=True,
                        help='ssh password')
    parser.add_argument('-v', dest='verbose', action="store_true",
                        help='show verbose output from provisioning')
    parser.add_argument('-q', dest='quiet', action="store_true",
                        help='show much less output, only errors')
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
        p.msg('   {:16s} {:30s} {}'.format(s.host, t, 'executing'))
        result, output, errors = s.execute_task(os.path.join(options.directory, t))

        if options.verbose and output:
            p.msg(' {} {:16s} {:30s} verbose: {}'.format('*', s.host, t, output))

        # If script writes to stderr but exits 0, interpret that as a user message
        if result and errors and not options.quiet:
            p.msg('   {:16s} {:30s} {}'.format(s.host, t, p.orange(errors)))

        # If the provisioning script didn't exit 0, then abort
        elif not result:
            p.err('   {:16s} {:30s} {}'.format(s.host, t, p.red(errors)))
            s.disconnect()
            p.msg(' {} {:16s} Disconnected'.format(p.green('*'), s.host))
            return

    p.msg(' {} {:16s} Disconnected'.format(p.green('*'), s.host))
    s.disconnect()


def main():
    """ Run provisioning scripts on a multiple servers simultaneously. """
    options = get_options()
    p = Message(options.quiet)

    auth = Auth()
    auth.set_username(options.username)
    auth.set_password(options.password)

    # provision multiple servers in parallel
    processes = []
    for server in options.ipaddr:
        proc = Process(target=provision_server, args=(p, server, options, auth))
        proc.start()
        processes.append(proc)

    for proc in processes:
        proc.join()


if __name__ == "__main__":
    main()
