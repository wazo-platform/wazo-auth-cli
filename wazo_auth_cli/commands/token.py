# Copyright 2017-2018 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

import json

from cliff.command import Command


class TokenCreate(Command):
    "Create new token"

    def get_parser(self, *args, **kwargs):
        parser = super().get_parser(*args, **kwargs)
        parser.add_argument('--expiration', help="Expiration of the token")
        parser.add_argument('--refresh_token', help="The refresh token to renew the token")
        parser.add_argument('--access_type', help="Access type: online or offline")
        parser.add_argument('--client_id', help="The client ID of the refresh token")
        return parser

    def take_action(self, parsed_args):
        params = {'expiration': 3600}
        if self.app.options.backend:
            params['backend'] = self.app.options.backend
        if parsed_args.expiration:
            params['expiration'] = parsed_args.expiration
        if parsed_args.access_type:
            params['access_type'] = parsed_args.access_type
        if parsed_args.refresh_token:
            params['refresh_token'] = parsed_args.refresh_token
        if parsed_args.client_id:
            params['client_id'] = parsed_args.client_id
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


class RefreshTokenList(Command):
    "List refresh token information"

    def get_parser(self, *args, **kwargs):
        parser = super().get_parser(*args, **kwargs)
        parser.add_argument('identifier', help='UUID of the user or me')
        return parser

    def take_action(self, parsed_args):
        token = self.app.client.token.list(user_uuid=parsed_args.identifier)
        self.app.stdout.write(json.dumps(token, indent=True, sort_keys=True) + '\n')


class RefreshTokenDelete(Command):
    "Delete a refresh token"

    def get_parser(self, *args, **kwargs):
        parser = super().get_parser(*args, **kwargs)
        parser.add_argument('--user_uuid', help='User UUID of the user or me')
        parser.add_argument('--client_id', help='Client ID of the refresh token')
        return parser

    def take_action(self, parsed_args):
        self.app.client.token.delete(user_uuid=parsed_args.user_uuid, client_id=parsed_args.client_id)


class TokenRevoke(Command):
    "Revoke token"

    def get_parser(self, *args, **kwargs):
        parser = super().get_parser(*args, **kwargs)
        parser.add_argument('identifier', help='token')
        return parser

    def take_action(self, parsed_args):
        self.app.client.token.revoke(parsed_args.identifier)
