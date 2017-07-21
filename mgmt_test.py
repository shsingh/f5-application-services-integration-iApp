#!/usr/bin/env python
import argparse
import sys

from src.appservices.BIPClient import BIPClient
from src.appservices.TestTools import get_test_config
from src.appservices.TestTools import prepare_payloads_functional_test
from src.appservices.TestTools import run_functional_tests
from src.appservices.tools import fix_indents as as_fix_indents
from src.appservices.tools import setup_logging


def fix_indents(path):
    as_fix_indents(path)


def get_version(host):
    bip = BIPClient(host)
    print(bip.get_version())


def run_test(host, policy_host):
    bip = BIPClient(host)
    config = get_test_config(host, policy_host, "manual")
    prepare_payloads_functional_test(bip, config)
    run_functional_tests(bip, config)


def get_parser():
    parser = argparse.ArgumentParser()

    parser.add_argument('-v', '--version',
                        help='BIP version',
                        action="store_true")
    parser.add_argument('host',
                        help='IP Address of BigIP to be tested')
    parser.add_argument("-b", "--policy_host",
                        help="The host to use for URL based bundled items")
    parser.add_argument("-l", "--log_cfg_file",
                        default="logging.yaml",
                        help="Logging configuration file")

    return parser


def router(parser, argv):
    args = parser.parse_args()
    if len(argv) < 1:
        parser.print_help()
        sys.exit(1)

    setup_logging(args.log_cfg_file)

    if args.version:
        get_version(args.host)

    if args.host and args.policy_host:
        run_test(args.host, args.policy_host)


if __name__ == "__main__":
    parser = get_parser()
    router(parser, sys.argv)
