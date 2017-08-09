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
import json
import logging
import os
import threading
from glob import glob

from src.appservices.PayloadGenerator import PayloadGenerator
from src.appservices.exceptions import AppServiceDeploymentException
from src.appservices.exceptions import AppServiceDeploymentVerificationException
from src.appservices.exceptions import AppServiceRemovalException
from src.appservices.exceptions import RESTException
from src.appservices.exceptions import ParameterMissingException
from src.appservices.tools import get_timestamp


def prepare_bip(bip):
    bip.upload_files(
        ['resources/test_config.conf'],
        ['/var/tmp/test_config.conf']
    )

    bip.run_command('tmsh -c \"delete ltm pool all;'
                    ' delete ltm node all\"')

    bip.run_command('tmsh load sys config file /var/tmp/test_config.conf merge')

    return bip.get_version(), bip.get_template_name()


def build_application_service_payloads(
        config, version, tcl_template_name="dummy"):

    pay_gen = PayloadGenerator(
        os.getcwd(),
        config['payloads_dir'],
        config['tmp_dir'],
        config['flat_templates_dir']
    )

    for payload_template in glob(
            os.path.join("payload_templates", "*.template.json")):
        pay_gen.fill_template(
            payload_template, version, config['policy_host'],
            config['vs_subnet'],
            config['vs_v6_subnet'],
            config['vs_first_address'],
            config['vs_v6_first_address'],
            config['member_subnet'],
            config['member_v6_subnet'],
            config['member_first_address'],
            config['member_v6_first_address'])

    for payload_template in glob(os.path.join(config['tmp_dir'], "*.tmpl")):
        pay_gen.build_template(
            config['tmp_dir'],
            payload_template,
            'admin',
            'admin'
        )

    for payload_template in glob(os.path.join(
            config['flat_templates_dir'], "*.tmpl")):
        pay_gen.build_bip_payload(payload_template, tcl_template_name)

    return pay_gen.find_dependent_payloads(config)


def prepare_payloads_functional_test(bip, config):
    version, tcl_template_name = prepare_bip(bip)
    return build_application_service_payloads(
        config, version, tcl_template_name)


def get_test_config(
        host, policy_host, no_delete=False, run_count=1, retries=1, ignore="",
        start=0, end=-1,
        vs_subnet="172.16.0.0/24",
        vs_first_address="172.16.0.100",
        vs_v6_subnet="2001:dead:beef:1::/120",
        vs_v6_first_address="2001:dead:beef:1::10",
        member_subnet="10.0.0.0/24",
        member_first_address="10.0.0.10",
        member_v6_subnet="2001:dead:beef:2::/120",
        member_v6_first_address="2001:dead:beef:2::10",
        test_method='pytest', timestamp=None):

    if host is None or host == "":
        raise ParameterMissingException('host')

    if policy_host is None or policy_host == "":
        raise ParameterMissingException('policy_host')

    if timestamp is None:
        timestamp = get_timestamp()

    session_id = "{}_{}".format(test_method, timestamp)
    config = {
        'timestamp': timestamp,
        'payloads_dir': os.path.abspath(
            os.path.join("logs", session_id, 'payloads')),
        'tmp_dir': os.path.abspath(os.path.join("logs", session_id, 'tmp')),
        'flat_templates_dir': os.path.abspath(os.path.join(
            "logs", session_id, 'payload_templates')),
        'host': host,
        'policy_host': policy_host,
        'session_id': session_id,
        'no_delete': no_delete,
        'run_count': run_count,
        'retries': retries,
        'ignore': ignore,
        'start': start,
        'end': end,
        'vs_subnet': vs_subnet,
        'vs_first_address': vs_first_address,
        'vs_v6_subnet': vs_v6_subnet,
        'vs_v6_first_address': vs_v6_first_address,
        'member_subnet': member_subnet,
        'member_first_address': member_first_address,
        'member_v6_subnet': member_v6_subnet,
        'member_v6_first_address': member_v6_first_address
    }
    return config


def handle_configuration_payload(config, bip, payload_basename, payload,
                                 test_run_log_dir, payload_dependencies):
    logger = logging.getLogger(__name__)

    for run in range(config['retries']):
        try:
            logger.info('{}/{} Deploying: {}'.format(
                run, config['retries'], payload_basename))

            app_deployed = bip.deploy_app_service(payload)

            logger.info('{}/{} Verifying deployment of: {}'.format(
                run, config['retries'], payload_basename))

            deployment_verified = bip.verify_deployment_result(
                payload, test_run_log_dir)

            if check_delete_override(
                    payload_dependencies, payload_basename):
                logger.info("Skipping removal of {},"
                            " due to 'test_delete_override'"
                            " flag set in payload template".format(
                    payload_basename))
            else:
                logger.info("{}/{} Removing payload {}".format(
                    run, config['retries'], payload_basename))
                bip.remove_app_service(payload)

            if app_deployed and deployment_verified:
                break

        except (AppServiceDeploymentException,
                RESTException,
                AppServiceDeploymentVerificationException,
                AppServiceRemovalException) as ex:
            logger.exception(ex)
            bip.download_logs(test_run_log_dir)
            bip.download_qkview(test_run_log_dir)
            if run+1 == config['retries']:
                raise


def run_legacy_functional_tests(bip_client, config, dependants):
    logger = logging.getLogger(__name__)

    for payload_file in get_payload_files(config):

        payload = load_payload(config, payload_file)
        payload_basename = get_payload_basename(payload_file)

        payload_dependencies = get_payload_dependencies(
            dependants, payload_basename)

        test_run_log_dir = os.path.abspath(
            os.path.join("logs", config['session_id'],
                         'run', payload['name'])
        )

        logger.debug('Testing payload {}'.format(payload_basename))
        handle_configuration_payload(config, bip_client, payload_basename, payload,
                                     test_run_log_dir, payload_dependencies)


def get_payload_dependencies(dependants, payload_name):
    for key, value in dependants.iteritems():
        if payload_name == key:
            return value
        for element in value:
            if element['name'] == payload_name:
                return value[value.index(element):]

    return []


def check_delete_override(dependencies, payload_name):
    for dependency in dependencies:
        if dependency['name'] == payload_name:
            return dependency['delete_override']

    return False


def get_payload_template_basename(name):
    return os.path.splitext(
        get_payload_basename(name)
    )[0]


def get_payload_basename(name):
    return os.path.splitext(os.path.basename(name))[0]


def payload_is_build_in(payload_file):
    payload_template_basename = get_payload_template_basename(payload_file)

    return os.path.isfile(
        os.path.join(
            os.path.abspath('payload_templates'),
            "{}.template.json".format(payload_template_basename)
        )
    )


def update_payload_name(name, run):
    name_split = name.split("__")
    try:
        int(name_split[-1])
        name_split[-1] = str(run)
        return "__".join(name_split)
    except ValueError:
        return "{}__{}".format(name, run)


def strip_payload_name(name):
    name_split = name.split("__")
    try:
        int(name_split[-1])
        return "__".join(name_split[:-1])
    except ValueError:
        return name


def get_payload_files(config):
    payloads = sorted(glob(os.path.join(config['payloads_dir'], "*.json")))
    return payloads[config['start']:config['end']]


def load_payloads(config, dependencies):
    payloads = []
    for dependency in dependencies:
        payloads.append(load_payload(
            config, "{}.json".format(dependency['name'])))

    return payloads


def load_payload(config, filename='test_monitors.json'):
    with open(os.path.join(config['payloads_dir'], filename)) as payload:
        data = json.load(payload)
    return data


class IappWorker(threading.Thread):
    def __init__(self, bip_client, payload, log_dir, results, thread_no):
        threading.Thread.__init__(self)
        self.bip_client = bip_client
        self.payload = payload
        self.log_dir = log_dir
        self.results = results
        self.thread_no = thread_no
        self.logger = logging.getLogger(__name__)

    def run(self):
        try:
            self.bip_client.deploy_app_service(self.payload)
            self.results[self.thread_no] = {
                'result': True,
                'msg': ''
            }

        except (RESTException, AppServiceDeploymentException) as ex:
            self.bip_client.download_logs(self.log_dir)
            self.results[self.thread_no] = {
                'result': False,
                'msg': ex
            }

        finally:
            return self.results
