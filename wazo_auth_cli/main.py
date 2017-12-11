# Copyright 2017 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

import logging
import sys

from cliff.app import App
from cliff.command import Command
from cliff.commandmanager import CommandManager

logger = logging.getLogger(__name__)


class UserCreate(Command):

    def take_action(self, parsed_args):
        logger.info('Creating user...')


class WazoAuthCLI(App):

    def __init__(self):
        super().__init__(
            description='A CLI for the wazo-auth service',
            command_manager=CommandManager('wazo_auth_cli.commands'),
            version='0.0.1',
        )

    def initialize_app(self, argv):
        self.LOG.debug('Wazo Auth CLI')

    def prepare_to_run_command(self, cmd):
        self.LOG.debug('prepare_to_run_command %s', cmd.__class__.__name__)

    def clean_up(self, cmd, result, err):
        self.LOG.debug('cleanup %s', cmd.__class__.__name__)
        if err:
            self.LOG.debug('got an error: %s', err)


def main(argv=sys.argv[1:]):
    app = WazoAuthCLI()
    return app.run(argv)


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
