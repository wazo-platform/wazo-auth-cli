# Copyright 2018-2020 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

import json

from cliff.command import Command
from cliff.lister import Lister

from ..helpers import TenantIdentifierMixin, UserIdentifierMixin, ListBuildingMixin


class TenantAdd(TenantIdentifierMixin, UserIdentifierMixin, Command):
    "Add tenant to a user"

    def get_parser(self, *args, **kwargs):
        parser = super().get_parser(*args, **kwargs)
        relation = parser.add_mutually_exclusive_group(required=True)
        relation.add_argument(
            '--user', help='The username or UUID of the user to add to this tenant'
        )
        parser.add_argument('identifier', help='name or UUID of the tenant')
        return parser

    def take_action(self, parsed_args):
        uuid = self.get_tenant_uuid(self.app.client, parsed_args.identifier)

        if parsed_args.user:
            return self._add_user(uuid, parsed_args)

    def _add_user(self, uuid, parsed_args):
        user_uuid = self.get_user_uuid(self.app.client, parsed_args.user)
        self.app.client.tenants.add_user(uuid, user_uuid)


class TenantCreate(TenantIdentifierMixin, Command):
    "Create new tenant"

    def get_parser(self, prog_name):
        parser = super(TenantCreate, self).get_parser(prog_name)
        parser.add_argument('--parent', help="The tenant's parent name or UUID")
        parser.add_argument('name', help="the tenant's name")
        return parser

    def take_action(self, parsed_args):
        self.app.LOG.debug(parsed_args)
        body = {
            'name': parsed_args.name,
        }

        if parsed_args.parent:
            parent_uuid = self.get_tenant_uuid(self.app.client, parsed_args.parent)
            body['parent_uuid'] = parent_uuid

        self.app.LOG.debug('Creating tenant %s', body)
        tenant = self.app.client.tenants.new(**body)
        self.app.LOG.info(tenant)
        self.app.stdout.write(tenant['uuid'] + '\n')


class TenantDelete(TenantIdentifierMixin, UserIdentifierMixin, Command):
    "Delete tenant"

    def get_parser(self, *args, **kwargs):
        parser = super().get_parser(*args, **kwargs)
        parser.add_argument(
            'identifier', help="The tenant or UUID of the tenant to delete"
        )
        return parser

    def take_action(self, parsed_args):
        uuid = self.get_user_uuid(self.app.client, parsed_args.identifier)
        self.app.LOG.debug('Deleting tenant %s', uuid)
        self.app.client.tenants.delete(uuid)


class TenantRemove(TenantIdentifierMixin, UserIdentifierMixin, Command):
    "Remove tenant to user"

    def get_parser(self, *args, **kwargs):
        parser = super().get_parser(*args, **kwargs)
        relation = parser.add_mutually_exclusive_group(required=True)
        relation.add_argument(
            '--user', help='The username or UUID of the user to remove from this tenant'
        )
        parser.add_argument('identifier', help='name or UUID of the tenant')
        return parser

    def take_action(self, parsed_args):
        uuid = self.get_tenant_uuid(self.app.client, parsed_args.identifier)

        if parsed_args.user:
            return self._remove_user(uuid, parsed_args)

    def _remove_user(self, uuid, parsed_args):
        user_uuid = self.get_user_uuid(self.app.client, parsed_args.user)
        self.app.client.tenants.remove_user(uuid, user_uuid)


class TenantList(ListBuildingMixin, Lister):
    "List tenants"

    _columns = ['uuid', 'name', 'contact', 'phone', 'parent_uuid']
    _removed_columns = ['address']

    def take_action(self, parsed_args):
        result = self.app.client.tenants.list()
        if not result['items']:
            return (), ()

        headers = self.extract_column_headers(result['items'][0])
        items = self.extract_items(headers, result['items'])
        return headers, items


class TenantShow(TenantIdentifierMixin, UserIdentifierMixin, Command):
    "Show tenant informations"

    def get_parser(self, *args, **kwargs):
        parser = super().get_parser(*args, **kwargs)
        parser.add_argument('identifier', help='tenant or UUID')
        return parser

    def take_action(self, parsed_args):
        uuid = self.get_tenant_uuid(self.app.client, parsed_args.identifier)
        tenant = self.app.client.tenants.get(uuid)
        self.app.stdout.write(json.dumps(tenant, indent=True, sort_keys=True) + '\n')
