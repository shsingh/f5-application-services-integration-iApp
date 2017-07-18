#!/usr/bin/env python
import argparse
import json
import logging
import os
import sys
from glob import glob

from src.appservices.BIPClient import BIPClient
from src.appservices.PayloadGenerator import PayloadGenerator
from src.appservices.TestTools import prepare_payloads_functional_test
from src.appservices.tools import fix_indents as as_fix_indents
from src.appservices.tools import get_timestamp


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
    bip = BIPClient(host, logging.basicConfig(level=logging.DEBUG))
    print(bip.get_version())


def run_test(host):
    logging.basicConfig(level=logging.DEBUG)
    bip_client = BIPClient(host, logging)
    timestamp = get_timestamp()
    session_id = "manual_{}".format(timestamp)
    config = {
        'timestamp': get_timestamp(),
        'payloads_dir': os.path.abspath(
            os.path.join("logs", session_id, 'payloads')),
        'tmp_dir': os.path.abspath(os.path.join("logs", session_id, 'tmp')),
        'flat_templates_dir': os.path.abspath(os.path.join(
            "logs", session_id, 'payload_templates')),
        'host': host,
        'policy_host': "10.144.72.137"
    }
    prepare_payloads_functional_test(config)

    for payload_file in sorted(glob(os.path.join(
            config['payloads_dir'], "*.json"))):
        with open(payload_file, 'r') as payload_file_handle:
            payload = json.load(payload_file_handle)

            assert bip_client.deploy_app_service(payload)
            assert bip_client.remove_app_service(payload)


def get_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--build_templates',
                        help='Build templates')
    parser.add_argument('-v', '--version',
                        help='BIP version',)
    parser.add_argument('-f', '--fix_indents',
                        help="fix indents")
    parser.add_argument('-r', '--run',
                        help='Run test')
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

    if args.run:
        run_test(args.run)


if __name__ == "__main__":
    parser = get_parser()
    router(parser, sys.argv)
