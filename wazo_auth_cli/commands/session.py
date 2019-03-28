# Copyright 2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

import json

from cliff.command import Command
from cliff.lister import Lister

from ..helpers import ListBuildingMixin


class SessionList(ListBuildingMixin, Lister):
    "List sessions"

    _columns = ['uuid', 'tenant_uuid', 'user_uuid', 'mobile']

    def take_action(self, parsed_args):
        result = self.app.client.sessions.list()
        if not result['items']:
            return (), ()

        headers = self.extract_column_headers(result['items'][0])
        items = self.extract_items(headers, result['items'])
        return headers, items


class SessionShow(Command):
    "Show user session informations"

    def get_parser(self, *args, **kwargs):
        parser = super().get_parser(*args, **kwargs)
        parser.add_argument('identifier', help='UUID')
        return parser

    def take_action(self, parsed_args):
        session = self.app.client.users.get_sessions(parsed_args.identifier)
        self.app.stdout.write(json.dumps(session, indent=True, sort_keys=True) + '\n')
