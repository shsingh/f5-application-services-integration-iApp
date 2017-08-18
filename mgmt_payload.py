#!/usr/bin/env python
# Copyright (c) 2017 F5 Networks, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
#     Unless required by applicable law or agreed to in writing, software
#     distributed under the License is distributed on an "AS IS" BASIS,
#     WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#     See the License for the specific language governing permissions and
#     limitations under the License.
#

import argparse
import logging
import os
import sys
from glob import glob
from pprint import pprint

from src.appservices.BIPClient import BIPClient
from src.appservices.TestTools import get_payload_dependencies
from src.appservices.TestTools import get_payload_template_basename
from src.appservices.TestTools import get_test_config
from src.appservices.TestTools import load_payload
from src.appservices.TestTools import load_payloads
from src.appservices.TestTools import payload_is_build_in
from src.appservices.TestTools import prepare_payloads_functional_test
from src.appservices.exceptions import AppServiceDeploymentException
from src.appservices.exceptions import AppServiceDeploymentVerificationException
from src.appservices.exceptions import AppServiceRemovalException
from src.appservices.exceptions import RESTException
from src.appservices.tools import setup_logging


def cli_parser():
    parser = argparse.ArgumentParser(
        description='This script uses the F5 BIG-IP iControl REST API'
                    ' to create a specific instance of an iApp deployment.')

    parser.add_argument("-H", "--host",
                        help="The IP/Hostname in <host>[:<port>]"
                             " format of the BIG-IP device")
    parser.add_argument("-P", "--payload",
                        help="The Application Services configuration payload")
    parser.add_argument("-X", "--remove",
                        help="Remove application Service")

    parser.add_argument("-l", "--list",
                        help="List default Application Services templates",
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

    return parser


def router(parser, argv):
    if len(argv) < 2:
        parser.print_help()
        sys.exit(1)

    args = parser.parse_args()

    setup_logging()

    if not args.remove and args.host and args.payload:
        upload_application_service(
            args.host, args.username, args.password, args.ssh_username,
            args.ssh_password, args.payload)

    if args.list:
        list_available_payload_templates()

    if args.remove and args.host:
        remove_application_service(
            args.host, args.username, args.password, args.ssh_username,
            args.ssh_password, args.remove
        )


def list_available_payload_templates():
    for index, payload_template in enumerate(sorted(
            glob(os.path.join("payload_templates", "*.template.json")))):
        print("{}\t{}".format(index, os.path.basename(payload_template)))


def remove_application_service(
        host, username, password, ssh_username, ssh_password, payload_file):
    bip_client = BIPClient(
        host, username=username, password=password,
        ssh_username=ssh_username, ssh_password=ssh_password)

    try:
        if payload_is_build_in(payload_file):
            bip_client, payload = load_build_in_payload(
                host, bip_client, payload_file)
            bip_client.remove_app_service(payload)
        else:
            bip_client.remove_app_service(load_payload(
                os.path.dirname(payload_file),
                os.path.basename(payload_file)
            ))

    except RESTException as error:
        logger.exception(error)
        sys.exit(1)


def upload_application_service(
        host, username, password, ssh_username, ssh_password, payload_file):
    bip = BIPClient(
        host, username=username, password=password,
        ssh_username=ssh_username, ssh_password=ssh_password)

    if payload_is_build_in(payload_file):
        bip, payload = load_build_in_payload(host, bip, payload_file)
        upload_payload(bip, payload)
    else:
        upload_payload(bip, load_payload(
            os.path.dirname(payload_file),
            os.path.basename(payload_file)
        ))


def yes_no_prompt(question):
    yes = set(['yes', 'y', 'ye', ''])
    no = set(['no', 'n'])

    while True:
        choice = raw_input(question).lower()
        if choice in yes:
            return True
        elif choice in no:
            return False
        else:
            print("Please respond with 'yes' or 'no'\n")


def load_build_in_payload(host, bip, payload_template_file):
    config = get_test_config(host, "127.0.0.1", test_method="manual",
                             timestamp=__name__)

    dependants = prepare_payloads_functional_test(bip, config)
    payload_basename = get_payload_template_basename(payload_template_file)
    payload_dependencies = get_payload_dependencies(
        dependants, payload_basename)

    if len(payload_dependencies) > 0:
        print('Due to a bug in BIP,'
              ' following payloads depend on the one you choose:')
        pprint(payload_dependencies)
        if yes_no_prompt("Deploy all y/n?"):
            return bip, load_payloads(config, payload_dependencies)

    payload_file = "{}.json".format(payload_basename)

    return bip, load_payload(config, payload_file)


def upload_payload(bip, payloads):

    logger = logging.getLogger(__name__)
    if not isinstance(payloads, (list, tuple)):
        payloads = [payloads]

    for payload in payloads:
        try:
            bip.deploy_app_service(payload)
        except (AppServiceDeploymentException,
                RESTException,
                AppServiceDeploymentVerificationException,
                AppServiceRemovalException) as ex:
            logger.exception(ex)
            sys.exit(1)


if __name__ == '__main__':
    router(cli_parser(), sys.argv)
