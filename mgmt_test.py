#!/usr/bin/env python
import sys
import os
import argparse
from glob import glob
from src.PayloadGenerator import PayloadGenerator
from src.AppServicesTools import fix_indents as as_fix_indents
from src.AppServicesTools import BIPClient


def build_templates(host):
    pay_gen = PayloadGenerator(os.getcwd())
    bip = BIPClient(host)
    version = bip.get_version()

    for payload_template in glob(os.path.join("payload_templates", "*.tmpl")):
        pay_gen.fill_template(
            payload_template, 123456, version, "10.144.72.137",
            u"172.16.0.0/24",
            u"2001:dead:beef:1::/120",
            u"172.16.0.100",
            u"2001:dead:beef:1::10",
            u"10.0.0.0/24",
            u"2001:dead:beef:2::/120",
            u"10.0.0.10",
            u"2001:dead:beef:2::10")


def fix_indents(path):
    as_fix_indents(path)


def get_version(host):
    bip = BIPClient(host)
    # print(bip.get_version())
    #
    # result = bip.run_command('tmsh -c \"delete ltm pool all;'
    #                          ' delete ltm node all\"')
    # print(result)
    # bip.upload_files(
    #     ['upload_files/test_config.conf'],
    #     ['/var/tmp/test_config.conf']
    # )

    pay_gen = PayloadGenerator(os.getcwd())
    tmpl = pay_gen.build_template(
        "tmp", "test_monitors.tmpl.123456.tmp", "admin", "admin")

    template_name = bip.get_template_name()

    payload = pay_gen.build_payload(
        tmpl, template_name, 'test_monitors.json', 'payloads_new')

    url = bip.deploy_app_service(payload)

    # bip.remove_app_service(payload['partition'], payload['name'])


def get_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--build_templates',
                        help='Build templates')
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
        build_templates(args.build_templates)

    if args.fix_indents:
        fix_indents(args.fix_indents)

    if args.version:
        get_version(args.version)


if __name__ == "__main__":
    parser = get_parser()
    router(parser, sys.argv)
