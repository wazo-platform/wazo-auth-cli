# Copyright 2017 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

import argparse
import logging

logger = logging.getLogger(__name__)


def main():
    args = parse_cli_args()
    log_level = logging.DEBUG if args.debug else logging.INFO
    logging.basicConfig(format='%(message)s', level=log_level)
    logger.debug('Wazo Auth CLI')
    logger.debug('processing: %s %s %s', args.object_, args.action, args.name)


def parse_cli_args():
    parser = argparse.ArgumentParser(prog='wazo-auth-cli')
    parser.add_argument('-d', '--debug', action='store_true', help='If the cli should be verbose')
    parser.add_argument('object_', metavar='object', type=str, help='The kind of object to operate on')
    parser.add_argument('action', type=str, help='The action to apply to the object')
    parser.add_argument('name', type=str, help='The name of the object to work on')
    return parser.parse_args()


if __name__ == '__main__':
    main()
