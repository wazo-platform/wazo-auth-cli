#!/usr/bin/env python3
# Copyright 2017-2018 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from setuptools import setup
from setuptools import find_packages


setup(
    name='wazo-auth-cli',
    version='1.0',
    author='Wazo Authors',
    author_email='dev@wazo.community',
    url='http://wazo.community',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'wazo-auth-cli = wazo_auth_cli.main:main',
        ],
        'wazo_auth_cli.commands': [
            'policy_create = wazo_auth_cli.commands.policy:PolicyCreate',
            'policy_delete = wazo_auth_cli.commands.policy:PolicyDelete',
            'policy_list = wazo_auth_cli.commands.policy:PolicyList',
            'policy_show = wazo_auth_cli.commands.policy:PolicyShow',
            'user_add = wazo_auth_cli.commands.user:UserAdd',
            'user_create = wazo_auth_cli.commands.user:UserCreate',
            'user_delete = wazo_auth_cli.commands.user:UserDelete',
            'user_list = wazo_auth_cli.commands.user:UserList',
            'user_remove = wazo_auth_cli.commands.user:UserRemove',
            'user_show = wazo_auth_cli.commands.user:UserShow',
            'tenant_add = wazo_auth_cli.commands.tenant:TenantAdd',
            'tenant_create = wazo_auth_cli.commands.tenant:TenantCreate',
            'tenant_remove = wazo_auth_cli.commands.tenant:TenantRemove',
            'tenant_delete = wazo_auth_cli.commands.tenant:TenantDelete',
            'tenant_list = wazo_auth_cli.commands.tenant:TenantList',
            'tenant_show = wazo_auth_cli.commands.tenant:TenantShow',
            'token_create = wazo_auth_cli.commands.token:TokenCreate',
            'token_show = wazo_auth_cli.commands.token:TokenShow',
            'token_revoke = wazo_auth_cli.commands.token:TokenRevoke',
            'group_add = wazo_auth_cli.commands.group:GroupAdd',
            'group_create = wazo_auth_cli.commands.group:GroupCreate',
            'group_delete = wazo_auth_cli.commands.group:GroupDelete',
            'group_show = wazo_auth_cli.commands.group:GroupShow',
            'group_list = wazo_auth_cli.commands.group:GroupList',
            'group_remove = wazo_auth_cli.commands.group:GroupRemove',
        ],
    },
)
