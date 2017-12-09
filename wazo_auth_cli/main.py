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


def parse_cli_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--debug', action='store_true', help='If the cli should be verbose')
    return parser.parse_args()


if __name__ == '__main__':
    main()
