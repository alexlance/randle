import paramiko
import time
import argparse
import sys
import os
from message import Message


class Auth():
    def setUsername(self, username):
        self.username = username

    def setPassword(self, password):
        self.password = password
        self.authType = 'password'

    def setPrivateKey(self, keyFile, passphrase):
        self.keyFile = keyFile
        self.authType = 'privateKey'

    def toDict(self):
        if self.authType == "password":
            return { 'username': self.username, 'password': self.password }
        elif self.authType == "privateKey":
            return { 'username': self.username, 'key_filename': self.keyFile }


class Server():
    CONN_CLOSED, CONN_OPEN, CONN_FAILED = 1, 2, 3

    def __init__(self, host, auth):
        self.host = host
        self.auth = auth
        self.connStatus = self.CONN_CLOSED
        self.ssh = None

    def connect(self):
        try:
            self.ssh = paramiko.SSHClient()
            self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            credentials = self.auth.toDict()
            credentials.update({ 'hostname': self.host })
            self.ssh.connect(**credentials)
            self.connStatus = self.CONN_OPEN
        except paramiko.AuthenticationException:
            self.connStatus = self.CONN_FAILED
        except e:
            raise e

    def disconnect(self):
        if self.connStatus == self.CONN_OPEN:
            self.ssh.close()
            self.connStatus = self.CONN_CLOSED

    def execute_task(self, filename):
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


def get_options():
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
    return parser.parse_args()


def check_config(p, path):
    for d in ['pre-hook', 'post-hook', 'server-todo', 'server-done']:
        if not os.path.isdir(os.path.join(path, d)):
            p.err('Missing directory: {}'.format(d))
            sys.exit(1)

    for f in sorted(os.listdir(os.path.join(path, 'server-todo'))):
        if not os.path.isfile(os.path.join(path, 'server-done', f)):
            p.err('File not found: {}'.format(os.path.join(path, 'server-done', f)))
            p.err('  (this means {} will execute on every run)'.format(os.path.join(path, 'server-todo', f)))

    for f in sorted(os.listdir(os.path.join(path, 'server-done'))):
        if not os.path.isfile(os.path.join(path, 'server-todo', f)):
            p.err('File not found: {}'.format(os.path.join(path, 'server-todo', f)))


    

def main():
  p = Message()
  options = get_options()
  check_config(p, options.PATH_TO_DEPLOY) 

  auth = Auth()
  auth.setUsername(options.username)
  auth.setPassword(options.password)

  for server in options.ipaddr:
      s = Server(server, auth)
      s.connect()
      if s.connStatus == s.CONN_OPEN:
          p.msg('{}: Connected'.format(s.host))
      elif s.connStatus == s.CONN_FAILED:
          p.die('{}: Authentication failed'.format(s.host))

      tasks = sorted(os.listdir(os.path.join(options.PATH_TO_DEPLOY, 'server-done')))
      for t in tasks:
          done_exit, done_output, done_errors = s.execute_task(os.path.join(options.PATH_TO_DEPLOY, 'server-done', t))
          if done_exit:
              p.warn('{}: Skipping {}'.format(s.host, t))
          else:
              p.halfmsg('   {}: Executing {} ...'.format(s.host, os.path.join(options.PATH_TO_DEPLOY, 'server-todo', t)))
              todo_exit, todo_output, todo_errors = s.execute_task(os.path.join(options.PATH_TO_DEPLOY, 'server-todo', t))
              if todo_exit:
                  p.yay('success'.format(s.host, t))
              else:
                  p.err('FAILED'.format(s.host, t))
                  if todo_errors:
                      p.err(todo_errors)

      s.disconnect()

   
main()
  

