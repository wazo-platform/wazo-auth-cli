# Copyright 2017-2018 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

import json

from cliff.command import Command


class TokenCreate(Command):
    "Create new token"

    def take_action(self, parsed_args):
        params = {'expiration': 3600}
        if self.app.options.backend:
            params['backend'] = self.app.options.backend
        token_data = self.app.client.token.new(**params)
        self.app.LOG.info(token_data)
        self.app.stdout.write(token_data['token'] + '\n')


class TokenShow(Command):
    "Show token informations"

    def get_parser(self, *args, **kwargs):
        parser = super().get_parser(*args, **kwargs)
        parser.add_argument('identifier', help='token')
        return parser

    def take_action(self, parsed_args):
        token = self.app.client.token.get(parsed_args.identifier)
        self.app.stdout.write(json.dumps(token, indent=True, sort_keys=True) + '\n')


class TokenRevoke(Command):
    "Revoke token"

    def get_parser(self, *args, **kwargs):
        parser = super().get_parser(*args, **kwargs)
        parser.add_argument('identifier', help='token')
        return parser

    def take_action(self, parsed_args):
        self.app.client.token.revoke(parsed_args.identifier)
