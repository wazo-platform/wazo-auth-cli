#!/usr/bin/env python3
# Copyright 2017-2024 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later


from setuptools import find_packages, setup

setup(
    name='wazo-auth-cli',
    version='1.0',
    author='Wazo Authors',
    author_email='dev@wazo.community',
    url='http://wazo.community',
    packages=find_packages(),
    entry_points={
        'console_scripts': ['wazo-auth-cli = wazo_auth_cli.main:main'],
        'wazo_auth_cli.commands': [
            'group_add = wazo_auth_cli.commands.group:GroupAdd',
            'group_create = wazo_auth_cli.commands.group:GroupCreate',
            'group_delete = wazo_auth_cli.commands.group:GroupDelete',
            'group_show = wazo_auth_cli.commands.group:GroupShow',
            'group_list = wazo_auth_cli.commands.group:GroupList',
            'group_remove = wazo_auth_cli.commands.group:GroupRemove',
            'ldap_config_update = wazo_auth_cli.commands.ldap_config:LDAPConfigUpdate',
            'ldap_config_show = wazo_auth_cli.commands.ldap_config:LDAPConfigShow',
            'ldap_config_delete = wazo_auth_cli.commands.ldap_config:LDAPConfigDelete',
            'policy_create = wazo_auth_cli.commands.policy:PolicyCreate',
            'policy_delete = wazo_auth_cli.commands.policy:PolicyDelete',
            'policy_list = wazo_auth_cli.commands.policy:PolicyList',
            'policy_show = wazo_auth_cli.commands.policy:PolicyShow',
            'user_add = wazo_auth_cli.commands.user:UserAdd',
            'user_create = wazo_auth_cli.commands.user:UserCreate',
            'user_update = wazo_auth_cli.commands.user:UserUpdate',
            'user_delete = wazo_auth_cli.commands.user:UserDelete',
            'user_list = wazo_auth_cli.commands.user:UserList',
            'user_remove = wazo_auth_cli.commands.user:UserRemove',
            'user_password = wazo_auth_cli.commands.user:UserSetPassword',
            'user_show = wazo_auth_cli.commands.user:UserShow',
            'session_list = wazo_auth_cli.commands.session:SessionList',
            'session_delete = wazo_auth_cli.commands.session:SessionDelete',
            'session_show = wazo_auth_cli.commands.session:SessionShow',
            'session_wipe = wazo_auth_cli.commands.session:SessionWipe',
            'tenant_add = wazo_auth_cli.commands.tenant:TenantAdd',
            'tenant_create = wazo_auth_cli.commands.tenant:TenantCreate',
            'tenant_remove = wazo_auth_cli.commands.tenant:TenantRemove',
            'tenant_delete = wazo_auth_cli.commands.tenant:TenantDelete',
            'tenant_list = wazo_auth_cli.commands.tenant:TenantList',
            'tenant_show = wazo_auth_cli.commands.tenant:TenantShow',
            'token_create = wazo_auth_cli.commands.token:TokenCreate',
            'token_refresh_list = wazo_auth_cli.commands.token:RefreshTokenList',
            'token_refresh_delete = wazo_auth_cli.commands.token:RefreshTokenDelete',
            'token_show = wazo_auth_cli.commands.token:TokenShow',
            'token_revoke = wazo_auth_cli.commands.token:TokenRevoke',
        ],
    },
    install_requires=[
        "wazo-auth-client@https://github.com/wazo-platform/wazo-auth-client/archive/master.zip",
        "xivo@https://github.com/wazo-platform/xivo-lib-python/archive/master.zip",
        "cliff>=3.4.0",
        "requests>=2.25.1",
        "pyyaml>=5.3.1",
    ],
)
