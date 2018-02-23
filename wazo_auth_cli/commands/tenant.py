# Copyright 2018 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

from cliff.command import Command

from ..helpers import TenantIdentifierMixin, UserIdentifierMixin


class TenantAdd(TenantIdentifierMixin, UserIdentifierMixin, Command):

    def get_parser(self, *args, **kwargs):
        parser = super().get_parser(*args, **kwargs)
        relation = parser.add_mutually_exclusive_group(required=True)
        relation.add_argument('--user',
                              help='The username or UUID of the user to add to this tenant')
        parser.add_argument('identifier', help='name or UUID of the tenant')
        return parser

    def take_action(self, parsed_args):
        uuid = self.get_tenant_uuid(self.app.client, parsed_args.identifier)

        if parsed_args.user:
            return self._add_user(uuid, parsed_args)

    def _add_user(self, uuid, parsed_args):
        user_uuid = self.get_user_uuid(self.app.client, parsed_args.user)
        self.app.client.tenants.add_user(uuid, user_uuid)


class TenantCreate(Command):

    def get_parser(self, prog_name):
        parser = super(TenantCreate, self).get_parser(prog_name)
        parser.add_argument('name', help="the tenant's name")
        return parser

    def take_action(self, parsed_args):
        self.app.LOG.debug(parsed_args)
        body = dict(
            name=parsed_args.name,
        )

        self.app.LOG.debug('Creating tenant %s', body)
        tenant = self.app.client.tenants.new(**body)
        self.app.LOG.info(tenant)
        self.app.stdout.write(tenant['uuid'] + '\n')


class TenantRemove(TenantIdentifierMixin, UserIdentifierMixin, Command):

    def get_parser(self, *args, **kwargs):
        parser = super().get_parser(*args, **kwargs)
        relation = parser.add_mutually_exclusive_group(required=True)
        relation.add_argument('--user',
                              help='The username or UUID of the user to remove from this tenant')
        parser.add_argument('identifier', help='name or UUID of the tenant')
        return parser

    def take_action(self, parsed_args):
        uuid = self.get_tenant_uuid(self.app.client, parsed_args.identifier)

        if parsed_args.user:
            return self._remove_user(uuid, parsed_args)

    def _remove_user(self, uuid, parsed_args):
        user_uuid = self.get_user_uuid(self.app.client, parsed_args.user)
        self.app.client.tenants.remove_user(uuid, user_uuid)
