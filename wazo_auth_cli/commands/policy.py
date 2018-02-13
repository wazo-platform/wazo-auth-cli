# Copyright 2017-2018 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

import json
import requests

from cliff.command import Command
from cliff.lister import Lister

from ..helpers import ListBuildingMixin, PolicyIdentifierMixin


class PolicyCreate(PolicyIdentifierMixin, Command):

    def get_parser(self, *args, **kwargs):
        parser = super().get_parser(*args, **kwargs)
        parser.add_argument('--description', help='the policy description')
        parser.add_argument('--acl', nargs='+', help='acl to assign to the new policy')
        parser.add_argument('--or-show', action='store_true',
                            help='show the policy UUID if this policy name already exists')
        parser.add_argument('name', help='the policy name')
        return parser

    def take_action(self, parsed_args):
        self.app.LOG.debug('Creating a new policy %s', parsed_args.name)
        self.app.LOG.debug('%s', parsed_args.acl)

        try:
            policy = self.app.client.policies.new(
                parsed_args.name,
                parsed_args.description,
                parsed_args.acl,
            )
            self.app.LOG.info(policy)
            self.app.stdout.write(policy['uuid'] + '\n')
        except requests.HTTPError as e:
            if parsed_args.or_show and e.response.status_code == 409:
                uuid = self.get_policy_uuid(self.app.client, parsed_args.name)
                return self.app.stdout.write(uuid + '\n')

            raise


class PolicyList(ListBuildingMixin, Lister):

    _columns = ['uuid', 'name', 'description']
    _removed_columns = ['acl_templates']

    def take_action(self, parsed_args):
        result = self.app.client.policies.list()
        if not result['items']:
            return (), ()

        headers = self.extract_column_headers(result['items'][0])
        items = self.extract_items(headers, result['items'])
        return headers, items


class PolicyShow(PolicyIdentifierMixin, Command):

    def get_parser(self, *args, **kwargs):
        parser = super().get_parser(*args, **kwargs)
        parser.add_argument('identifier', help='name or UUID')
        return parser

    def take_action(self, parsed_args):
        uuid = self.get_policy_uuid(self.app.client, parsed_args.identifier)
        policy = self.app.client.policies.get(uuid)
        self.app.stdout.write(json.dumps(policy, indent=True, sort_keys=True) + '\n')
