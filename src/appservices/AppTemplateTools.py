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

import logging


def load_template_parts(impl, apl, script, html, macro):
    logger = logging.getLogger(__name__)
    result = {
        'impl': None,
        'apl': None,
        'script': None,
        'help': None,
        'macro': None
    }

    # Get data from the file containing implementation layer
    #  TCL code (-i argument)
    with open(impl) as impl_file:
        result['impl'] = impl_file.read()

    # Get data from the file containing presentation layer
    #  APL code (-a argument)
    with open(apl) as apl_file:
        result['apl'] = apl_file.read()

    # OPTIONAL: Get data from the file containing utilities
    #  tcl procedures code (-s argument)
    try:
        with open(script) as script_file:
            result['script'] = script_file.read()
    except IOError:
        logger.warning("CLI script file \"{}\" not found,"
                       " setting to blank".format(script))
        result['script'] = ""

    # OPTIONAL: Get data from the file containing HTML Help (-n argument)
    try:
        with open(html) as help_file:
            result['help'] = help_file.read()
    except IOError:
        logger.warning("HTML Help file \"{}\" not found,"
                       " setting to blank".format(html))
        result['help'] = ""

    # OPTIONAL: Get data from the file containing the iApp macro (-m argument)
    try:
        with open(macro) as macro_file:
            result['macro'] = macro_file.read()
    except IOError:
        logger.warning("Macro file \"{}\" not found,"
                       " setting to blank".format(macro))
        result['macro'] = ""

    return result


def get_template_deploy_payload(minver, maxver, modules, name, data):
    return {
        "ignoreVerification": "false",
        "requiresBigipVersionMin": minver,
        "requiresBigipVersionMax": maxver,
        "requiresModules": modules.split(','),
        "name": name,
        "actions": [
            {
                "name": "definition",
                "roleAcl": ["admin", "manager", "resource-admin"],
                "implementation": data['impl'],
                "presentation": data['apl'],
                "htmlHelp": data['help'],
                "macro": data['macro']
            }
        ]
    }


def get_definition_payload(data):
    return {
        "implementation": data['impl'],
        "presentation": data['apl'],
        "htmlHelp": data['help'],
        "macro": data['macro']
    }


def get_cli_script_deploy_payload(script_name, data):
    return {
        "name": script_name,
        "partition": "Common",
        "apiAnonymous": data['script'],
        "ignoreVerification": "false",
        "totalSigningStatus": "not-all-signed"
    }


def get_cli_script_update_payload(script_name, data):
    return {
        "name": script_name,
        "apiAnonymous": data['script']
    }
