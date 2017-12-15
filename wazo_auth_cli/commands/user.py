# Copyright 2017 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

import json

from cliff.command import Command


class UserCreate(Command):

    def get_parser(self, prog_name):
        parser = super(UserCreate, self).get_parser(prog_name)
        parser.add_argument('--passwd', help="The user's password", action='store')
        parser.add_argument('--email', help="The user's main email address", required=True)
        parser.add_argument('name', help="The user's username")
        return parser

    def take_action(self, parsed_args):
        body = dict(
            username=parsed_args.name,
            email_address=parsed_args.email,
            password=parsed_args.passwd,
        )
        self.app.LOG.debug('Creating user %s', body)

        user = self.app.client.users.new(**body)
        data = json.dumps(user)
        self.app.LOG.info(data)
        self.app.stdout.write(user['uuid'] + '\n')
