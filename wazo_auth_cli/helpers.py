# Copyright 2017-2023 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from uuid import UUID


def is_uuid(string):
    try:
        UUID(string)
    except Exception:
        return False

    return True


class ListBuildingMixin:
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


class TenantIdentifierMixin:
    def get_tenant_uuid(self, client, identifier):
        if is_uuid(identifier):
            return identifier

        result = client.tenants.list(name=identifier)
        if not result['items']:
            raise Exception(f'Unknown tenant "{identifier}"')

        return result['items'][0]['uuid']


class GroupIdentifierMixin:
    def get_group_uuid(self, client, identifier):
        if is_uuid(identifier):
            return identifier

        result = client.groups.list(name=identifier)
        if not result['items']:
            raise Exception(f'Unknown group "{identifier}"')

        return result['items'][0]['uuid']


class UserIdentifierMixin:
    def get_user_uuid(self, client, identifier):
        if is_uuid(identifier):
            return identifier

        result = client.users.list(username=identifier, recurse=True)
        if not result['items']:
            raise Exception(f'Unknown user "{identifier}"')

        return result['items'][0]['uuid']


class PolicyIdentifierMixin:
    def get_policy_uuid(self, client, identifier):
        if is_uuid(identifier):
            return identifier

        # TODO: update to use name=identifier once the client implements it and remove the loop
        result = client.policies.list(search=identifier, recurse=True)
        if not result['items']:
            raise Exception(f'Unknown policy "{identifier}"')

        for item in result['items']:
            if item['name'] == identifier:
                return item['uuid']

        raise Exception(f'Unknown policy "{identifier}"')
