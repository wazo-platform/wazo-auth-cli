# Copyright 2017 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+
import logging
logger = logging.getLogger(__name__)

from xivo.chain_map import ChainMap
from xivo.config_helper import parse_config_dir, read_config_file_hierarchy


_APP_NAME = 'wazo-auth-cli'
_DEFAULT_AUTH_CONFIG = dict(
    host='localhost',
    port=9497,
    verify_certificate=True,
)
_DEFAULT_CONFIG = dict(
    config_file='/etc/{}/config.yml'.format(_APP_NAME),
    extra_config_files='/etc/{}/conf.d/'.format(_APP_NAME),
    auth=_DEFAULT_AUTH_CONFIG,
)

_AUTH_ARGS_TO_FIELDS_MAP = dict(
    auth_username='username',
    hostname='host',
    auth_password='password',
    port='port',
)


def _args_to_dict(parsed_args):
    auth_config = dict()
    for arg_name, config_name in _AUTH_ARGS_TO_FIELDS_MAP.items():
        value = getattr(parsed_args, arg_name, None)
        if value is None:
            continue
        logger.debug('setting %s = %s', config_name, value)
        auth_config[config_name] = value

    if parsed_args.verify:
        auth_config['verify_cerficate'] = True
    elif parsed_args.insecure:
        auth_config['verify_certificate'] = False
    elif parsed_args.cacert:
        auth_config['verify_certificate'] = parsed_args.cacert

    config = dict(auth=auth_config)
    return config


def _read_user_config(parsed_args):
    if not parsed_args.config:
        return {}
    configs = parse_config_dir(parsed_args.config)
    return ChainMap(*configs)


def build(parsed_args):
    cli_config = _args_to_dict(parsed_args)
    user_file_config = _read_user_config(parsed_args)
    system_file_config = read_config_file_hierarchy(ChainMap(cli_config, user_file_config, _DEFAULT_CONFIG))
    final_config = ChainMap(cli_config, user_file_config, system_file_config, _DEFAULT_CONFIG)
    return final_config
