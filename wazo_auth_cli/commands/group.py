# Copyright 2018-2023 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

import json

from cliff.command import Command
from cliff.lister import Lister

from ..helpers import (
    GroupIdentifierMixin,
    ListBuildingMixin,
    TenantIdentifierMixin,
    UserIdentifierMixin,
)


class GroupAdd(GroupIdentifierMixin, UserIdentifierMixin, Command):
    "Associate a group to another resource"

    def get_parser(self, *args, **kwargs):
        parser = super().get_parser(*args, **kwargs)
        relation = parser.add_mutually_exclusive_group(required=True)
        relation.add_argument(
            '--user', help='The username of UUID of the user to add to this group'
        )
        parser.add_argument('identifier', help='name of UUID of the group')
        return parser

    def take_action(self, parsed_args):
        uuid = self.get_group_uuid(self.app.client, parsed_args.identifier)

        if parsed_args.user:
            return self._add_user(uuid, parsed_args)

    def _add_user(self, uuid, parsed_args):
        user_uuid = self.get_user_uuid(self.app.client, parsed_args.user)
        self.app.client.groups.add_user(uuid, user_uuid)


class GroupRemove(GroupIdentifierMixin, UserIdentifierMixin, Command):
    "Dissociate a group to another resource"

    def get_parser(self, *args, **kwargs):
        parser = super().get_parser(*args, **kwargs)
        relation = parser.add_mutually_exclusive_group(required=True)
        relation.add_argument(
            '--user', help='The username of UUID of the user to add to this group'
        )
        parser.add_argument('identifier', help='name of UUID of the group')
        return parser

    def take_action(self, parsed_args):
        uuid = self.get_group_uuid(self.app.client, parsed_args.identifier)

        if parsed_args.user:
            return self._remove_user(uuid, parsed_args)

    def _remove_user(self, uuid, parsed_args):
        user_uuid = self.get_user_uuid(self.app.client, parsed_args.user)
        self.app.client.groups.remove_user(uuid, user_uuid)


class GroupCreate(TenantIdentifierMixin, Command):
    "Create new group"

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument('name', help="the group's name")
        parser.add_argument('--tenant', help="The user's tenant")
        return parser

    def take_action(self, parsed_args):
        self.app.LOG.debug(parsed_args)
        body = {'name': parsed_args.name}

        if parsed_args.tenant:
            tenant_uuid = self.get_tenant_uuid(self.app.client, parsed_args.tenant)
            body['tenant_uuid'] = tenant_uuid

        self.app.LOG.debug('Creating group %s', body)
        group = self.app.client.groups.new(**body)
        self.app.LOG.info(group)
        self.app.stdout.write(group['uuid'] + '\n')


class GroupDelete(Command):
    "Delete group"

    def get_parser(self, *args, **kwargs):
        parser = super().get_parser(*args, **kwargs)
        parser.add_argument('identifier', help="The group or UUID to delete")
        return parser

    def take_action(self, parsed_args):
        uuid = parsed_args.identifier
        self.app.LOG.debug('Deleting tenant %s', uuid)
        self.app.client.groups.delete(uuid)


class GroupList(TenantIdentifierMixin, ListBuildingMixin, Lister):
    "List groups"

    _columns = ['uuid', 'name']

    def get_parser(self, *args, **kwargs):
        parser = super().get_parser(*args, **kwargs)
        parser.add_argument(
            '--recurse', help='Show users in all subtenants', action='store_true'
        )
        parser.add_argument('--tenant', help="Show users in a specific tenant")
        return parser

    def take_action(self, parsed_args):
        kwargs = {}
        if parsed_args.recurse:
            kwargs['recurse'] = parsed_args.recurse
        if parsed_args.tenant:
            kwargs['tenant_uuid'] = self.get_tenant_uuid(
                self.app.client, parsed_args.tenant
            )

        result = self.app.client.groups.list(**kwargs)
        if not result['items']:
            return (), ()

        headers = self.extract_column_headers(result['items'][0])
        items = self.extract_items(headers, result['items'])
        return headers, items


class GroupShow(GroupIdentifierMixin, Command):
    "Show group informations"

    def get_parser(self, *args, **kwargs):
        parser = super().get_parser(*args, **kwargs)
        parser.add_argument('identifier', help='group or UUID')
        return parser

    def take_action(self, parsed_args):
        uuid = self.get_group_uuid(self.app.client, parsed_args.identifier)
        group = self.app.client.groups.get(uuid)
        group['users'] = self.app.client.groups.get_users(uuid)
        self.app.stdout.write(json.dumps(group, indent=True, sort_keys=True) + '\n')
