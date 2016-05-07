""" Generic user message printing. """

import sys


class Message(object):
    """ A class to funnel all user messages through. """

    def __init__(self, quiet=False, debug=False):
        self.quiet = quiet
        self.debug = debug

    def msg(self, s):
        """ Print a message to the screen (stdout). """
        if not self.quiet:
            print str(s)
            sys.stdout.flush()

    def err(self, s):
        """ Print a failure message to the screen (stderr). """
        sys.stderr.write(str(s)+"\n")

    def die(self, s):
        """ Print a failure message to the screen (stderr) and then halt. """
        self.err(s)
        sys.exit(1)

    def dbg(self, s):
        """ Print a message to the screen (stdout) for debugging only. """
        if self.debug:
            print "DBG " + str(s)
            sys.stdout.flush()

    def green(self, s):
        """ Change text colour - should find more generic method. """
        return '\033[92m{}\033[0m'.format(s)

    def orange(self, s):
        """ Change text colour - should find more generic method. """
        return '\033[93m{}\033[0m'.format(s)

    def red(self, s):
        """ Change text colour - should find more generic method. """
        return '\033[91m{}\033[0m'.format(s)
