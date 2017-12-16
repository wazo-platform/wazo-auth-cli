# Copyright 2017 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

from cliff.command import Command
from cliff.lister import Lister


class UserCreate(Command):

    def get_parser(self, prog_name):
        parser = super(UserCreate, self).get_parser(prog_name)
        parser.add_argument('--password', help="the user's password", required=True)
        parser.add_argument('--email', help="the user's main email address", required=True)
        parser.add_argument('name', help="the user's username")
        return parser

    def take_action(self, parsed_args):
        self.app.LOG.debug(parsed_args)
        body = dict(
            username=parsed_args.name,
            email_address=parsed_args.email,
            password=parsed_args.password,
        )
        self.app.LOG.debug('Creating user %s', body)

        user = self.app.client.users.new(**body)
        self.app.LOG.info(user)
        self.app.stdout.write(user['uuid'] + '\n')


class UserDelete(Command):

    def get_parser(self, *args, **kwargs):
        parser = super().get_parser(*args, **kwargs)
        parser.add_argument('uuid', help="The UUID of the user to delete")
        return parser

    def take_action(self, parsed_args):
        self.app.LOG.debug('Deleting user %s', parsed_args.uuid)
        self.app.client.users.delete(parsed_args.uuid)


class UserList(Lister):

    def take_action(self, parsed_args):
        result = self.app.client.users.list()
        if result['items']:
            headers = result['items'][0]
            users = []
            for u in result['items']:
                user = [u[h] for h in headers]
                users.append(user)
            return headers, users
        return (), ()
