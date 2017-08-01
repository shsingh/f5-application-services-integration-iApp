#!/usr/bin/env python

import argparse
import sys

from src.appservices.tools import setup_logging
from src.appservices.TestTools import get_test_config


def cli_parser():
    parser = argparse.ArgumentParser(
        description='This script uses the F5 BIG-IP iControl REST API'
                    ' to create a specific instance of an iApp deployment.')

    parser.add_argument("host",
                        help="The IP/Hostname in <host>[:<port>]"
                             " format of the BIG-IP device")
    parser.add_argument("-t", "--payload_template",
                        help="The *.tmpl iApp (payload template) file")
    parser.add_argument("-j", "--json_payload",
                        help="The *.json App Services payload")
    parser.add_argument("-X", "--remove",
                        help="Remove application Service",
                        action="store_true")

    parser.add_argument("-u", "--username",
                        help="The BIG-IP username",
                        default="admin")
    parser.add_argument("-p", "--password",
                        help="The BIG-IP password",
                        default="admin")
    parser.add_argument("--ssh_username",
                        help="The BIG-IP ssh username",
                        default="root")
    parser.add_argument("--ssh_password",
                        help="The BIG-IP ssh password",
                        default="default")
    parser.add_argument("--password-file",
                        help="The BIG-IP password stored in a file",
                        dest='password_file')

    parser.add_argument("-d", "--dontsave",
                        help="Don't automatically save the config",
                        action="store_true")
    parser.add_argument("-r", "--redeploy",
                        help="Redeploy an existing iApp",
                        action="store_true")

    parser.add_argument("-n", "--nocheck",
                        help="Don't check for deployment completion",
                        action="store_true")

    parser.add_argument("--iapp_name",
                        help="iapp_name (optional)")
    parser.add_argument("--strings",
                        help="override variables, i.e."
                             " --strings=pool_addr,172.16.0.231")
    parser.add_argument("--pool_members",
                        help="common separated list of ip:[port]"
                             " will replace \"0.0.0.0\" members")
    return parser


def router(parser, argv):
    if len(argv) < 2:
        parser.print_help()
        sys.exit(1)

    args = parser.parse_args()

    setup_logging()

    if not args.remove:
        upload_application_service(args.host)


def upload_application_service(host):
    #TODO
    pass


def load_payload(host, payload_template, json_paylod):
    #TODO
    pass

if __name__ == '__main__':
    router(cli_parser(), sys.argv)
