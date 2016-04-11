import sys


class Message():
    quiet = False

    def msg(self, s):
        # Print a message to the screen (stdout).
        if not self.quiet:
            print str(s)
            sys.stdout.flush()

    def yay(self, s):
        # Print a success message to the screen (stdout).
        if not self.quiet:
            print str(s)
            sys.stdout.flush()

    def warn(self, s):
        # Print a message to the screen (stdout).
        if not self.quiet:
            print str(s)
            sys.stdout.flush()

    def err(self, s):
        # Print a failure message to the screen (stderr).
        sys.stderr.write(str(s)+"\n")

    def die(self, s):
        # Print a failure message to the screen (stderr) and then halt.
        self.err(s)
        sys.exit(1)

    def dbg(self, s):
        # Print a message to the screen (stdout) for debugging only.
        if self.debug:
            print "DBG " + str(s)
            sys.stdout.flush()

    def green(self, s):
        return '\033[92m{}\033[0m'.format(s)

    def orange(self, s):
        return '\033[93m{}\033[0m'.format(s)

    def red(self, s):
        return '\033[91m{}\033[0m'.format(s)
