# Copyright 2017 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

from cliff.command import Command


class TokenCreate(Command):

    def take_action(self, parsed_args):
        backend = self.app.options.backend
        token_data = self.app.client.token.new(backend, expiration=3600)
        self.app.LOG.info(token_data)
        self.app.stdout.write(token_data['token'] + '\n')
