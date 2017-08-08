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
import sys

from src.appservices.AppTemplateTools import get_cli_script_deploy_payload
from src.appservices.AppTemplateTools import get_cli_script_update_payload
from src.appservices.AppTemplateTools import get_definition_payload
from src.appservices.AppTemplateTools import get_template_deploy_payload
from src.appservices.AppTemplateTools import load_template_parts
from src.appservices.BIPClient import BIPClient
from src.appservices.tools import setup_logging


def cli_parser():
    parser = argparse.ArgumentParser(
        description='BIG-IP REST client that automates the process of uploading'
                    ' the Application Service template.')
    parser.add_argument("host",
                        help="The IP/Hostname in <host>[:<port>] format of the BIG-IP device")
    parser.add_argument("name",
                        help="The name iApp template")
    parser.add_argument("-a", "--apl",
                        help="The path to the iApp apl layer file to import",
                        default="iapp.apl")
    parser.add_argument("-c", "--checkonly",
                        help="Only check to see if a template existings on the device",
                        action="store_true")
    parser.add_argument("-d", "--dontsave",
                        help="Don't automatically save the config",
                        action="store_true")
    parser.add_argument("-sn", "--script_name",
                        help="The name of iApp additional script",
                        default=None)
    parser.add_argument("-s", "--script",
                        help="The path to the iApp additional script to import",
                        default="appsvcs.integration.util.tcl")
    parser.add_argument("-i", "--impl",
                        help="The path to the iApp implementation layer file to import",
                        default="iapp.tcl")
    parser.add_argument("-m", "--macro",
                        help="The path to the iApp HTML help file to import",
                        default="iapp.macro")
    parser.add_argument("-n", "--html",
                        help="The path to the iApp HTML help file to import",
                        default="iapp.html")
    parser.add_argument("-o", "--overwrite",
                        help="Overwrite an existing template definitions",
                        action="store_true")
    parser.add_argument("-p", "--password",
                        help="The BIG-IP password",
                        default="admin")
    parser.add_argument("-r", "--modules",
                        help="The BIG-IP TMOS modules required (ex: ltm,gtm)",
                        default="")
    parser.add_argument("-u", "--username",
                        help="The BIG-IP username",
                        default="admin")
    parser.add_argument("-v", "--minver",
                        help="The minimum version of BIG-IP TMOS required",
                        default="11.0.0")
    parser.add_argument("-x", "--maxver",
                        help="The maximum version of BIG-IP TMOS required",
                        default="")
    parser.add_argument("--password-file",
                        help="The BIG-IP password stored in a file",
                        dest='password_file')
    return parser


def deploy_template_from_parts(
        impl, apl, script, html, macro, template_name, script_name, dont_save,
        host, username, password, overwrite, minver, maxver, modules):

    client = BIPClient(host, username=username, password=password)
    logger = logging.getLogger(__name__)

    template_exists = client.check_if_template_exists(template_name)
    if template_exists and not overwrite:
        logger.error(
            "A template named \"{}\" already exists on BIG-IP \"{}\". "
            "To overwrite please specify the '-o' flag".format(
                template_name, host))
        sys.exit(1)

    template_parts = load_template_parts(impl, apl, script, html, macro)
    payload = get_template_deploy_payload(
        minver, maxver, modules, template_name, template_parts)

    if template_exists:
        if not client.update_template(template_name, payload):
            logger.error("Base template properties update failed: {}")
            sys.exit(1)

        definition_payload = get_definition_payload(template_parts)
        if not client.update_template_definition(
                template_name, definition_payload):
            logger.error("Template definition properties update failed")
            sys.exit(1)
    else:
        if client.deploy_template(payload):
            print("[success] Template \"{}\" created on BIG-IP \"{}\"".format(
                template_name, host))
        else:
            logger.error("Template creation failed")

    if template_parts['script'] != '' and script_name:
        script_exists = client.cli_script_exists(script_name)

        print("script name {}".format(script_name))

        if script_exists and not overwrite:
            logger.error(
                "A cli script named \"{}\" already exists on BIG-IP \"{}\". "
                "To overwrite please specify the '-o' flag".format(
                    script_name, host))
            sys.exit(1)

        if script_exists:
            payload = get_cli_script_update_payload(
                script_name, template_parts)
            if not client.update_cli_script(script_name, payload):
                logger.error("Cli script update failed")
        else:
            payload = get_cli_script_deploy_payload(
                script_name, template_parts)
            if not client.deploy_cli_script(payload):
                logger.error("Cli script creation failed")

    if not dont_save:
        client.save_config()


def check_if_template_exists(host, username, password, template_name):
    client = BIPClient(host, username=username, password=password)
    logger = logging.getLogger(__name__)

    if client.check_if_template_exists(template_name):
        logger.info("Template '{}' exists on {}".format(template_name, host))
        sys.exit(1)
    else:
        logger.error("Template '{}' does not exist on {}".format(template_name, host))
        sys.exit(0)


def router(parser, argv):
    if len(argv) < 2:
        parser.print_help()
        sys.exit(1)

    args = parser.parse_args()

    setup_logging()

    if args.checkonly:
        check_if_template_exists(
            args.host, args.username, args.password, args.name)
    else:
        deploy_template_from_parts(
            args.impl, args.apl, args.script, args.html, args.macro, args.name,
            args.script_name, args.dontsave, args.host, args.username,
            args.password, args.overwrite, args.minver, args.maxver,
            args.modules
        )

if __name__ == '__main__':
    router(cli_parser(), sys.argv)
