# Copyright 2017 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

from uuid import UUID


def is_uuid(string):
    try:
        UUID(string)
    except Exception:
        return False

    return True


class ListBuildingMixin(object):

    _columns = []
    _removed_columns = []

    def extract_column_headers(self, item):
        headers = item.keys()
        missing_columns = set(headers) - set(self._columns) - set(self._removed_columns)
        columns = self._columns + list(missing_columns)
        return columns

    def extract_items(self, headers, items):
        results = []
        for item in items:
            result = [item[header] for header in headers]
            results.append(result)
        return results


class UserIdentifierMixin(object):

    def get_user_uuid(self, client, identifier):
        if is_uuid(identifier):
            return identifier

        result = client.users.list(username=identifier)
        if not result['items']:
            raise Exception('Unknown user "{}"'.format(identifier))

        return result['items'][0]['uuid']
