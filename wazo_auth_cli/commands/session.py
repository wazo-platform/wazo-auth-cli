# Copyright 2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

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
