# Copyright 2018 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

import json

from cliff.command import Command
from cliff.lister import Lister

from ..helpers import TenantIdentifierMixin, UserIdentifierMixin, ListBuildingMixin


class GroupCreate(Command):
    "Create new group"

    def get_parser(self, prog_name):
        parser = super(GroupCreate, self).get_parser(prog_name)
        parser.add_argument('name', help="the group's name")
        return parser

    def take_action(self, parsed_args):
        self.app.LOG.debug(parsed_args)
        body = dict(
            name=parsed_args.name,
        )

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


class GroupList(ListBuildingMixin, Lister):
    "List groups"

    _columns = ['uuid', 'name']

    def take_action(self, parsed_args):
        result = self.app.client.groups.list()
        if not result['items']:
            return (), ()

        headers = self.extract_column_headers(result['items'][0])
        items = self.extract_items(headers, result['items'])
        return headers, items


class GroupShow(Command):
    "Show group informations"

    def get_parser(self, *args, **kwargs):
        parser = super().get_parser(*args, **kwargs)
        parser.add_argument('identifier', help='group or UUID')
        return parser

    def take_action(self, parsed_args):
        uuid = parsed_args.identifier
        group = self.app.client.groups.get(uuid)
        self.app.stdout.write(json.dumps(group, indent=True, sort_keys=True) + '\n')
