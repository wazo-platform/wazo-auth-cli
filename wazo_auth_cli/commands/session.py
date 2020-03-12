# Copyright 2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

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
