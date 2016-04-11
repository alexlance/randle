import paramiko
import time

class Server(object):
    """ A class to model our provisioning of one particular server. """
    CONN_CLOSED, CONN_OPEN, CONN_FAILED = 1, 2, 3
    loop_counter = 0

    def __init__(self, host, auth):
        self.host = host
        self.auth = auth
        self.conn_status = self.CONN_CLOSED
        self.ssh = None

    def connect(self):
        """ Use the paramiko ssh library to create an ssh connection to a server. """
        try:
            self.ssh = paramiko.SSHClient()
            self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            credentials = self.auth.to_dict()
            credentials.update({'hostname': self.host})
            self.ssh.connect(**credentials)
            self.conn_status = self.CONN_OPEN
        except paramiko.AuthenticationException:
            self.conn_status = self.CONN_FAILED
        except paramiko.ssh_exception.SSHException:
            if self.loop_counter < 3:
                time.sleep(2)
                self.loop_counter += 1
                self.connect()

    def disconnect(self):
        """ Kill the ssh connection. """
        if self.conn_status == self.CONN_OPEN:
            self.ssh.close()
            self.conn_status = self.CONN_CLOSED

    def execute_task(self, filename):
        """ Run a local script on a remote server. """
        chan = self.ssh.get_transport().open_session()
        chan.exec_command(open(filename).read())
        output = ''
        errors = ''
        receiving = True
        while receiving:
            if chan.recv_ready():
                output += chan.recv(4096).decode('ascii')
            if chan.recv_stderr_ready():
                errors += chan.recv_stderr(4096).decode('ascii')
            if chan.exit_status_ready():
                receiving = False

        if chan.recv_exit_status() == 0:
            return True, output, errors
        else:
            return False, output, errors


