# Copyright 2019-2024 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

import json

from cliff.command import Command
from cliff.lister import Lister

from ..helpers import ListBuildingMixin, TenantIdentifierMixin


class SessionList(TenantIdentifierMixin, ListBuildingMixin, Lister):
    "List sessions"

    _columns = ['uuid', 'tenant_uuid', 'user_uuid', 'mobile']

    def get_parser(self, *args, **kwargs):
        parser = super().get_parser(*args, **kwargs)
        parser.add_argument(
            '--recurse', help='Show sessions in all subtenants', action='store_true'
        )
        parser.add_argument('--tenant', help="Show sessions in a specific tenant")
        return parser

    def take_action(self, parsed_args):
        kwargs = {
            'recurse': parsed_args.recurse,
        }

        if parsed_args.tenant:
            tenant_uuid = self.get_tenant_uuid(self.app.client, parsed_args.tenant)
            kwargs['tenant_uuid'] = tenant_uuid

        result = self.app.client.sessions.list(**kwargs)
        if not result['items']:
            return (), ()

        headers = self.extract_column_headers(result['items'][0])
        items = self.extract_items(headers, result['items'])
        return headers, items


class SessionDelete(Command):
    "Delete session"

    def get_parser(self, *args, **kwargs):
        parser = super().get_parser(*args, **kwargs)
        parser.add_argument('identifier', help="The UUID of the session to delete")
        return parser

    def take_action(self, parsed_args):
        session_uuid = parsed_args.identifier
        self.app.LOG.debug('Deleting session %s', session_uuid)
        self.app.client.sessions.delete(session_uuid)


class SessionShow(Command):
    "Show session informations"

    def get_parser(self, *args, **kwargs):
        parser = super().get_parser(*args, **kwargs)
        parser.add_argument('identifier', help='session UUID')
        return parser

    def take_action(self, parsed_args):
        sessions = self.app.client.sessions.list(recurse=True)
        for session in sessions['items']:
            if session['uuid'] == parsed_args.identifier:
                self.app.stdout.write(
                    json.dumps(session, indent=True, sort_keys=True) + '\n'
                )
                break


class SessionWipe(Command):
    "Wipes all user\'s sessions"

    def get_parser(self, *args, **kwargs):
        parser = super().get_parser(*args, **kwargs)
        parser.add_argument('identifier', help='user\'s UUID')
        return parser

    def take_action(self, parsed_args):
        user_uuid = parsed_args.identifier
        tenant_uuid = self.app.client.users.get(user_uuid=user_uuid)['tenant_uuid']
        sessions = self.app.client.sessions.list(tenant_uuid=tenant_uuid)

        sessions = [
            session
            for session in sessions['items']
            if session['user_uuid'] == user_uuid
        ]
        for session in sessions:
            self.app.LOG.debug('Deleting session %s', session['uuid'])
            self.app.client.sessions.delete(session['uuid'])

        self.app.stdout.write(
            f'Wiped {len(sessions)} sessions for user {user_uuid}\n',
        )
