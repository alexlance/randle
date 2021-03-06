""" Authentication wrapper for ssh. """


class Auth(object):
    """ Flexible method of handling multiple ssh auth methods. """

    def __init__(self):
        self.username = ''
        self.password = ''
        self.auth_type = ''
        self.key_file = ''
        self.passphrase = ''

    def set_username(self, username):
        """ Will need username for both password and private key auth. """
        self.username = username

    def set_password(self, password):
        """ For username and password authentication method. """
        self.password = password
        self.auth_type = 'password'

    def set_private_key(self, key_file, passphrase):
        """ Use a private key for ssh auth. Not implemented yet. """
        self.key_file = key_file
        self.passphrase = passphrase
        self.auth_type = 'private_key'

    def to_dict(self):
        """ Serialize credentials to dict for generic handling. """
        if self.auth_type == "password":
            return {'username': self.username, 'password': self.password}
        elif self.auth_type == "private_key":
            return {'username': self.username, 'key_filename': self.key_file}
