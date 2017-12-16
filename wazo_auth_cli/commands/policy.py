# Copyright 2017 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

from cliff.command import Command


class PolicyCreate(Command):

    def get_parser(self, *args, **kwargs):
        parser = super().get_parser(*args, **kwargs)
        parser.add_argument('--description', help='the policy description')
        parser.add_argument('--acl', nargs='+', help='acl to assign to the new policy')
        parser.add_argument('name', help='the policy name')
        return parser

    def take_action(self, parsed_args):
        self.app.LOG.debug('Creating a new policy %s', parsed_args.name)
        self.app.LOG.debug('%s', parsed_args.acl)

        policy = self.app.client.policies.new(
            parsed_args.name, parsed_args.description, parsed_args.acl)
        self.app.LOG.info(policy)
        self.app.stdout.write(policy['uuid'] + '\n')
