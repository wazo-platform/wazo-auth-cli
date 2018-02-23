# Copyright 2018 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

from cliff.command import Command


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
