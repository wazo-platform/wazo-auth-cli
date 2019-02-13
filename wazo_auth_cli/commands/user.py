# Copyright 2017-2018 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

import json

from cliff.command import Command
from cliff.lister import Lister

from ..helpers import (
    GroupIdentifierMixin,
    ListBuildingMixin,
    PolicyIdentifierMixin,
    TenantIdentifierMixin,
    UserIdentifierMixin,
)


class UserAdd(UserIdentifierMixin, PolicyIdentifierMixin, GroupIdentifierMixin, Command):
    "Add policy or/and group to a user"

    def get_parser(self, *args, **kwargs):
        parser = super().get_parser(*args, **kwargs)
        relation = parser.add_mutually_exclusive_group(required=True)
        relation.add_argument('--policy',
                              help='The name or UUID of the policy to add to this user')
        relation.add_argument('--group',
                              help='The name or UUID of the group to add to this user')
        parser.add_argument('identifier', help='username or UUID')
        return parser

    def take_action(self, parsed_args):
        uuid = self.get_user_uuid(self.app.client, parsed_args.identifier)

        if parsed_args.policy:
            return self._add_policy(uuid, parsed_args)

        if parsed_args.group:
            return self._add_group(uuid, parsed_args)

    def _add_policy(self, uuid, parsed_args):
        policy_uuid = self.get_policy_uuid(self.app.client, parsed_args.policy)
        self.app.client.users.add_policy(uuid, policy_uuid)

    def _add_group(self, uuid, parsed_args):
        group_uuid = self.get_group_uuid(self.app.client, parsed_args.group)
        self.app.client.groups.add_user(group_uuid, uuid)


class UserCreate(TenantIdentifierMixin, Command):
    "Add new user"

    def get_parser(self, prog_name):
        parser = super(UserCreate, self).get_parser(prog_name)
        parser.add_argument('--uuid', help="The user's UUID when matching a PBX user")
        parser.add_argument('--password', help="the user's password", required=True)
        parser.add_argument('--email', help="the user's main email address")
        parser.add_argument('--firstname', help="The user's firstname")
        parser.add_argument('--lastname', help="The user's lastname")
        parser.add_argument('--purpose', help="The user's purpose")
        parser.add_argument('--tenant', help="The user's tenant")
        parser.add_argument('name', help="the user's username")
        return parser

    def take_action(self, parsed_args):
        self.app.LOG.debug(parsed_args)
        body = dict(
            username=parsed_args.name,
            password=parsed_args.password,
        )
        if parsed_args.uuid:
            body['uuid'] = parsed_args.uuid
        if parsed_args.email:
            body['email_address'] = parsed_args.email
        if parsed_args.firstname:
            body['firstname'] = parsed_args.firstname
        if parsed_args.lastname:
            body['lastname'] = parsed_args.lastname
        if parsed_args.purpose:
            body['purpose'] = parsed_args.purpose
        if parsed_args.tenant:
            tenant_uuid = self.get_tenant_uuid(self.app.client, parsed_args.tenant)
            body['tenant_uuid'] = tenant_uuid

        self.app.LOG.debug('Creating user %s', body)
        user = self.app.client.users.new(**body)
        self.app.LOG.info(user)
        self.app.stdout.write(user['uuid'] + '\n')


class UserDelete(UserIdentifierMixin, Command):
    "Delete user"

    def get_parser(self, *args, **kwargs):
        parser = super().get_parser(*args, **kwargs)
        parser.add_argument('identifier', help="The username or UUID of the user to delete")
        return parser

    def take_action(self, parsed_args):
        uuid = self.get_user_uuid(self.app.client, parsed_args.identifier)
        self.app.LOG.debug('Deleting user %s', uuid)
        self.app.client.users.delete(uuid)


class UserList(TenantIdentifierMixin, ListBuildingMixin, Lister):
    "List users"

    _columns = ['uuid', 'username', 'email']
    _removed_columns = ['emails']

    def get_parser(self, *args, **kwargs):
        parser = super().get_parser(*args, **kwargs)
        parser.add_argument('--recurse', help='Show users in all subtenants', action='store_true')
        parser.add_argument('--tenant', help="Show users in a specific tenant")
        return parser

    def take_action(self, parsed_args):
        kwargs = {
            'recurse': parsed_args.recurse,
        }

        if parsed_args.tenant:
            tenant_uuid = self.get_tenant_uuid(self.app.client, parsed_args.tenant)
            kwargs['tenant_uuid'] = tenant_uuid

        result = self.app.client.users.list(**kwargs)
        if not result['items']:
            return (), ()

        raw_items = self._add_email_column(result['items'])
        headers = self.extract_column_headers(raw_items[0])
        items = self.extract_items(headers, raw_items)
        return headers, items

    def _add_email_column(self, items):
        for item in items:
            email = self._main_email(item['emails']) or self._first_email(item['emails'])
            item['email'] = email
        return items

    @staticmethod
    def _main_email(emails):
        for email in emails:
            if email['main']:
                return email['address']
        return ''

    @staticmethod
    def _first_email(emails):
        for email in emails:
            return email['address']
        return ''


class UserRemove(UserIdentifierMixin, PolicyIdentifierMixin, GroupIdentifierMixin, Command):
    "Remove policy or/and group to user"

    def get_parser(self, *args, **kwargs):
        parser = super().get_parser(*args, **kwargs)
        relation = parser.add_mutually_exclusive_group(required=True)
        relation.add_argument('--policy',
                              help='The name or UUID of the policy to remove from this user')
        relation.add_argument('--group',
                              help='The name or UUID of the group to remove from this user')
        parser.add_argument('identifier', help='username or UUID')
        return parser

    def take_action(self, parsed_args):
        uuid = self.get_user_uuid(self.app.client, parsed_args.identifier)

        if parsed_args.policy:
            return self._remove_policy(uuid, parsed_args)

        if parsed_args.group:
            return self._remove_group(uuid, parsed_args)

    def _remove_policy(self, uuid, parsed_args):
        policy_uuid = self.get_policy_uuid(self.app.client, parsed_args.policy)
        self.app.client.users.remove_policy(uuid, policy_uuid)

    def _remove_group(self, uuid, parsed_args):
        group_uuid = self.get_group_uuid(self.app.client, parsed_args.policy)
        self.app.client.groups.remove_user(group_uuid, uuid)


class UserShow(UserIdentifierMixin, Command):
    "Show user informations"

    def get_parser(self, *args, **kwargs):
        parser = super().get_parser(*args, **kwargs)
        parser.add_argument('identifier', help='username or UUID')
        return parser

    def take_action(self, parsed_args):
        uuid = self.get_user_uuid(self.app.client, parsed_args.identifier)
        user = self.app.client.users.get(uuid)
        user['policies'] = self.app.client.users.get_policies(uuid)['items']
        user['tenants'] = self.app.client.users.get_tenants(uuid)['items']
        user['groups'] = self.app.client.users.get_groups(uuid)['items']
        self.app.stdout.write(json.dumps(user, indent=True, sort_keys=True) + '\n')
