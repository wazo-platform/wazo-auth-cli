# Copyright 2022 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

import json

from cliff.command import Command

from ..helpers import TenantIdentifierMixin


class LDAPConfigUpdate(TenantIdentifierMixin, Command):
    """Update LDAP config"""

    def get_parser(self, *args, **kwargs):
        parser = super().get_parser(*args, **kwargs)
        parser.add_argument('host', help="Host of the ldap server")
        parser.add_argument('port', help="Port of the ldap server")
        parser.add_argument('--protocol_version', help="Version of ldap protocol")
        parser.add_argument('--protocol_security', help="Encryption options")
        parser.add_argument(
            '--bind_dn', help="DN to use to bind the service to the LDAP server"
        )
        parser.add_argument(
            '--bind_password', help="The password of the service account"
        )
        parser.add_argument(
            'user_base_dn', help='The base DN in which users are located'
        )
        parser.add_argument(
            'user_login_attribute', help='The attribute that identify users'
        )
        parser.add_argument(
            'user_email_attribute', help='The email attribute in ldap schema'
        )
        parser.add_argument('--tenant', help="The LDAP config's tenant")
        return parser

    def take_action(self, parsed_args):
        params = {}
        if parsed_args.host:
            params['host'] = parsed_args.host
        if parsed_args.port:
            params['port'] = parsed_args.port
        if parsed_args.protocol_version:
            params['protocol_version'] = parsed_args.protocol_version
        if parsed_args.protocol_security:
            params['protocol_security'] = parsed_args.protocol_security
        if parsed_args.bind_dn:
            params['bind_dn'] = parsed_args.bind_dn
        if parsed_args.bind_password:
            params['bind_password'] = parsed_args.bind_password
        if parsed_args.user_base_dn:
            params['user_base_dn'] = parsed_args.user_base_dn
        if parsed_args.user_login_attribute:
            params['user_login_attribute'] = parsed_args.user_login_attribute
        if parsed_args.user_email_attribute:
            params['user_email_attribute'] = parsed_args.user_email_attribute
        if parsed_args.tenant:
            tenant_uuid = self.get_tenant_uuid(self.app.client, parsed_args.tenant)
            params['tenant_uuid'] = tenant_uuid

        config_ldap = self.app.client.ldap_config.create(
            params, tenant_uuid=params.get('tenant_uuid')
        )
        self.app.LOG.info(config_ldap)


class LDAPConfigShow(TenantIdentifierMixin, Command):
    """Show ldap config information"""

    def get_parser(self, *args, **kwargs):
        parser = super().get_parser(*args, **kwargs)
        parser.add_argument('--tenant', help="The LDAP config's tenant")
        return parser

    def take_action(self, parsed_args):
        params = {}
        if parsed_args.tenant:
            tenant_uuid = self.get_tenant_uuid(self.app.client, parsed_args.tenant)
            params['tenant_uuid'] = tenant_uuid
        config_ldap = self.app.client.ldap_config.get(**params)
        self.app.stdout.write(
            json.dumps(config_ldap, indent=True, sort_keys=True) + '\n'
        )


class LDAPConfigDelete(Command):
    """Delete an ldap config"""

    def get_parser(self, *args, **kwargs):
        parser = super().get_parser(*args, **kwargs)
        parser.add_argument('--tenant', help="The LDAP config's tenant")
        return parser

    def take_action(self, parsed_args):
        params = {}
        if parsed_args.tenant:
            tenant_uuid = self.get_tenant_uuid(self.app.client, parsed_args.tenant)
            params['tenant_uuid'] = tenant_uuid
        self.app.client.ldap_config.delete(**params)
