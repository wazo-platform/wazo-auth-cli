# Copyright 2017 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

import sys

from cliff.app import App
from cliff.commandmanager import CommandManager
from xivo_auth_client import Client
from . import config

import logging
logging.getLogger('requests').setLevel(logging.ERROR)


class WazoAuthCLI(App):

    DEFAULT_VERBOSE_LEVEL = 0

    def __init__(self):
        super().__init__(
            description='A CLI for the wazo-auth service',
            command_manager=CommandManager('wazo_auth_cli.commands'),
            version='0.0.1',
        )
        self._current_token = None
        self._remove_token = False

    def build_option_parser(self, *args, **kwargs):
        parser = super(WazoAuthCLI, self).build_option_parser(*args, **kwargs)
        parser.add_argument('--config',
                            help='Extra configuration directory to override the system configuration')
        parser.add_argument('--hostname', help='The wazo-auth hostname')
        parser.add_argument('--port', help='The wazo-auth port')

        https_verification = parser.add_mutually_exclusive_group()
        https_verification.add_argument('--verify', action='store_true',
                                        help='Verify the HTTPS certificate or not')
        https_verification.add_argument('--insecure', action='store_true',
                                        help='Bypass certificate verification')
        https_verification.add_argument('--cacert', help='Specify the ca bundle file')

        auth_or_token = parser.add_mutually_exclusive_group()
        auth_or_token.add_argument('--token', help='The wazo-auth token to use')

        username_password = auth_or_token.add_argument_group()
        username_password.add_argument('--auth-username', metavar='auth_username',
                                       help='The username to use to retrieve a token')
        username_password.add_argument('--auth-password', metavar='auth_password',
                                       help='The password to use to retrieve a token')
        username_password.add_argument('--backend', help='The backend to use when authenticating')

        return parser

    def initialize_app(self, argv):
        self.LOG.debug('Wazo Auth CLI')
        self.LOG.debug('options=%s', self.options)
        conf = config.build(self.options)
        self.LOG.debug('Starting with config: %s', conf)

        self.LOG.debug('client args: %s', conf['auth'])
        self.client = Client(**conf['auth'])

        if self.options.token:
            self._auth_token = self.options.token
        else:
            token_data = self.client.token.new(self.options.backend, expiration=3600)
            self._auth_token = token_data['token']
            self._remove_token = True

        self.client.set_token(self._auth_token)

    def clean_up(self, cmd, result, err):
        if err:
            self.LOG.debug('got an error: %s', err)

        if self._remove_token:
            self.client.token.revoke(self._current_token)
            self._remove_token = False


def main(argv=sys.argv[1:]):
    app = WazoAuthCLI()
    return app.run(argv)


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
