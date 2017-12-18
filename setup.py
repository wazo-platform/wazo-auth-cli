#!/usr/bin/env python3
# Copyright 2017 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

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
            'policy_list = wazo_auth_cli.commands.policy:PolicyList',
            'user_create = wazo_auth_cli.commands.user:UserCreate',
            'user_delete = wazo_auth_cli.commands.user:UserDelete',
            'user_list = wazo_auth_cli.commands.user:UserList',
            'token_create = wazo_auth_cli.commands.token:TokenCreate',
        ],
    },
)
