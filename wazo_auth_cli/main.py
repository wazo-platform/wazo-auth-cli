# Copyright 2017 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

import argparse
import logging
import sys

logger = logging.getLogger(__name__)


class UnknownAction(Exception):

    _msg_fmt = 'Unknown action "{}.{}"'

    def __init__(self, object_, action):
        super().__init__(self._msg_fmt.format(object_, action))


class UnknownObject(Exception):

    _msg_fmt = 'Unknown object "{}"'

    def __init__(self, object_):
        super().__init__(self._msg_fmt.format(object_))


class UserHandler:

    def create(self, username, args):
        pass

command_handlers = dict(user=UserHandler)


def process_args(args):
    logger.debug('processing: %s %s %s', args.object_, args.action, args.name)
    Handler = command_handlers.get(args.object_)
    if not Handler:
        raise UnknownObject(args.object_)
    handler = Handler()
    fn = getattr(handler, args.action, None)
    if not fn:
        raise UnknownAction(args.object_, args.action)
    fn(args.name, args)


def main():
    args = parse_cli_args()
    log_level = logging.DEBUG if args.debug else logging.INFO
    logging.basicConfig(format='%(message)s', level=log_level)
    logger.debug('Wazo Auth CLI')
    try:
        process_args(args)
    except Exception as e:
        logger.error(str(e))
        sys.exit(1)


def parse_cli_args():
    parser = argparse.ArgumentParser(prog='wazo-auth-cli')
    parser.add_argument('-d', '--debug', action='store_true', help='If the cli should be verbose')
    parser.add_argument('object_', metavar='object', type=str, help='The kind of object to operate on')
    parser.add_argument('action', type=str, help='The action to apply to the object')
    parser.add_argument('name', type=str, help='The name of the object to work on')
    return parser.parse_args()


if __name__ == '__main__':
    main()
