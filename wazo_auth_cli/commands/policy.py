# Copyright 2017-2020 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

import json
import requests

from cliff.command import Command
from cliff.lister import Lister

from ..helpers import (
    ListBuildingMixin,
    PolicyIdentifierMixin,
    TenantIdentifierMixin,
)


class PolicyCreate(PolicyIdentifierMixin, TenantIdentifierMixin, Command):
    "Create policy"

    def get_parser(self, *args, **kwargs):
        parser = super().get_parser(*args, **kwargs)
        parser.add_argument('--description', help='the policy description')
        parser.add_argument(
            '--acl', nargs='+', default=[], help='acl to assign to the new policy'
        )
        parser.add_argument(
            '--or-show',
            action='store_true',
            help='show the policy UUID if this policy name already exists',
        )
        parser.add_argument('--tenant', help="The policy's tenant")
        parser.add_argument('name', help='the policy name')
        return parser

    def take_action(self, parsed_args):
        self.app.LOG.debug('Creating a new policy %s', parsed_args.name)
        self.app.LOG.debug('%s', parsed_args.acl)
        body = {
            'name': parsed_args.name,
            'description': parsed_args.description,
            'acl': parsed_args.acl,
        }

        if parsed_args.tenant:
            tenant_uuid = self.get_tenant_uuid(self.app.client, parsed_args.tenant)
            body['tenant_uuid'] = tenant_uuid

        try:
            policy = self.app.client.policies.new(**body)
            self.app.LOG.info(policy)
            self.app.stdout.write(policy['uuid'] + '\n')
        except requests.HTTPError as e:
            if parsed_args.or_show and e.response.status_code == 409:
                uuid = self.get_policy_uuid(self.app.client, parsed_args.name)
                return self.app.stdout.write(uuid + '\n')

            raise


class PolicyDelete(PolicyIdentifierMixin, Command):
    "Delete policy"

    def get_parser(self, *args, **kwargs):
        parser = super().get_parser(*args, **kwargs)
        parser.add_argument(
            'identifier', help="The name or UUID of the policy to delete"
        )
        return parser

    def take_action(self, parsed_args):
        uuid = self.get_policy_uuid(self.app.client, parsed_args.identifier)
        self.app.LOG.debug('Deleting policy %s', uuid)
        self.app.client.policies.delete(uuid)


class PolicyList(ListBuildingMixin, TenantIdentifierMixin, Lister):
    "List all policies available"

    _columns = ['uuid', 'name', 'description', 'tenant_uuid']
    _removed_columns = ['acl_templates', 'acl']

    def get_parser(self, *args, **kwargs):
        parser = super().get_parser(*args, **kwargs)
        parser.add_argument(
            '--recurse', help='Show policies in all subtenants', action='store_true'
        )
        parser.add_argument('--tenant', help="Show policies in a specific tenant")
        return parser

    def take_action(self, parsed_args):
        args = {}
        if parsed_args.tenant:
            tenant_uuid = self.get_tenant_uuid(self.app.client, parsed_args.tenant)
            args['tenant_uuid'] = tenant_uuid
        if parsed_args.recurse:
            args['recurse'] = True

        result = self.app.client.policies.list(**args)
        if not result['items']:
            return (), ()

        headers = self.extract_column_headers(result['items'][0])
        items = self.extract_items(headers, result['items'])
        return headers, items


class PolicyShow(PolicyIdentifierMixin, Command):
    "Show policy"

    def get_parser(self, *args, **kwargs):
        parser = super().get_parser(*args, **kwargs)
        parser.add_argument('identifier', help='name or UUID')
        return parser

    def take_action(self, parsed_args):
        uuid = self.get_policy_uuid(self.app.client, parsed_args.identifier)
        policy = self.app.client.policies.get(uuid)
        del policy['acl_templates']
        self.app.stdout.write(json.dumps(policy, indent=True, sort_keys=True) + '\n')
