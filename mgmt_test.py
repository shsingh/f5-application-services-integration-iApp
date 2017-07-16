#!/usr/bin/env python
import sys
import os
import argparse
from glob import glob
from src.PayloadGenerator import PayloadGenerator
from src.AppServicesTools import fix_indents as as_fix_indents
from src.AppServicesTools import BIPClient


def build_payloads():
    pay_gen = PayloadGenerator(os.getcwd())
    version = {
        'major': "1",
        'minor': "2",
        'version': "3"
    }
    for payload_template in glob(os.path.join("payload_templates", "*.tmpl")):
        pay_gen.build_template(
            payload_template, 123456, version, "10.144.72.137",
            u"172.16.0.0/24",
            u"2001:dead:beef:1::/120",
            u"10.0.0.0/24",
            u"2001:dead:beef:2::/120")


def fix_indents(path):
    as_fix_indents(path)


def get_version(host):
    bip = BIPClient(host)
    # print(bip.get_version())
    #
    # result = bip.run_command('tmsh -c \"delete ltm pool all;'
    #                          ' delete ltm node all\"')
    # print(result)
    bip.upload_files(
        ['upload_files/test_config.conf'],
        ['/var/tmp/test_config.conf']
    )


def get_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--build_templates',
                        help='Build templates',
                        action="store_true")
    parser.add_argument('-v', '--version',
                        help='BIP version',)
    parser.add_argument('-f', '--fix_indents',
                        help="fix indents")
    return parser


def router(parser, argv):
    args = parser.parse_args()
    if len(argv) < 2:
        parser.print_help()
        sys.exit(1)

    if args.build_templates:
        build_payloads()

    if args.fix_indents:
        fix_indents(args.fix_indents)

    if args.version:
        get_version(args.version)


if __name__ == "__main__":
    parser = get_parser()
    router(parser, sys.argv)
