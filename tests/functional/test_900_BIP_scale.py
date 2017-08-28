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

import ipaddress
import pytest

from src.appservices.TestTools import get_payload_basename
from src.appservices.TestTools import get_payload_dependencies
from src.appservices.TestTools import get_payload_files
from src.appservices.TestTools import load_payload
from src.appservices.TestTools import strip_payload_name
from src.appservices.TestTools import update_payload_name
from src.appservices.exceptions import AppServiceDeploymentException
from src.appservices.exceptions import AppServiceDeploymentVerificationException
from src.appservices.exceptions import AppServiceRemovalException
from src.appservices.exceptions import RESTException
from src.appservices.tools import mk_dir
from src.appservices.tools import save_json


@pytest.fixture(scope='module')
def get_scale_size(request):
    return request.config.getoption("--scale_size")


@pytest.fixture(scope='module')
def get_scale_long_run(request):
    return request.config.getoption("--scale_long_run")


def remove_application_service(
        deployment_no, payload, bip_client, test_results, scale_long_run):

    logger = logging.getLogger(__name__)

    for removal_no in range(deployment_no + 1):
        payload['name'] = update_payload_name(
            payload['name'], removal_no)
        try:
            bip_client.remove_app_service(payload)
        except RESTException as error:
            test_results[strip_payload_name(payload['name'])].setdefault(
                'removal_exception', []).append((removal_no, str(error)))
            logger.exception(error)
            if not scale_long_run:
                raise

    return test_results


def independent_scale(payload, first_pool_addr, log_dir, bip_client,
                      test_results, scale_size, scale_long_run):
    logger = logging.getLogger(__name__)

    for deployment_no in range(scale_size):
        payload['name'] = update_payload_name(
            payload['name'], deployment_no)
        logger.info("independent_scale: {}".format(payload['name']))

        payload["variables"][7]['value'] = str(
            first_pool_addr+deployment_no)

        test_run_log_dir = os.path.abspath(
            os.path.join(log_dir, strip_payload_name(payload['name']),
                         str(deployment_no))
        )

        try:
            bip_client.deploy_app_service(payload)
            bip_client.verify_deployment_result(
                payload, test_run_log_dir)
            test_results[strip_payload_name(
                payload['name'])]['completed'] = deployment_no + 1

        except (AppServiceDeploymentException, RESTException,
                AppServiceDeploymentVerificationException) as ex:
            test_results[strip_payload_name(payload['name'])].setdefault(
                'deployment_exception', []).append((deployment_no, str(ex)))
            logger.exception(ex)
            bip_client.download_logs(test_run_log_dir)
            bip_client.download_qkview(test_run_log_dir)
            if not scale_long_run:
                raise

    return remove_application_service(
        deployment_no, payload, bip_client, test_results, scale_long_run)


def dependent_scale(config, payload_dependencies, first_pool_addr, bip_client,
                    test_results, log_dir, scale_size, scale_long_run):
    logger = logging.getLogger(__name__)

    for deployment_no in range(scale_size):
        for index, dependency in enumerate(payload_dependencies):

            payload = load_payload(config, "{}.json".format(dependency['name']))
            logger.info('dependent_scale {}'.format(dependency['name']))

            payload['name'] = update_payload_name(
                payload['name'], deployment_no)

            if payload["variables"][7]['value'] == '172.16.0.100':
                payload["variables"][7]['value'] = str(
                    first_pool_addr+deployment_no)

            test_run_log_dir = os.path.abspath(
                os.path.join(log_dir, strip_payload_name(payload['name']),
                             str(deployment_no))
            )

            try:
                bip_client.deploy_app_service(payload)
                bip_client.verify_deployment_result(
                    payload, test_run_log_dir)
                test_results[strip_payload_name(
                    payload['name'])]['completed'] = deployment_no + 1

            except (AppServiceDeploymentException, RESTException,
                    AppServiceDeploymentVerificationException) as ex:
                test_results[strip_payload_name(payload['name'])].setdefault(
                    'deployment_exception', []).append((deployment_no, str(ex)))
                logger.exception(ex)
                bip_client.download_logs(test_run_log_dir)
                bip_client.download_qkview(test_run_log_dir)
                if not scale_long_run:
                    raise

            if not dependency['delete_override'] and (index+1) < len(
                    payload_dependencies):
                test_results = remove_application_service(
                    deployment_no, payload, bip_client, test_results,
                    scale_long_run)

    return remove_application_service(
        deployment_no, payload, bip_client, test_results, scale_long_run)


@pytest.mark.skipif(not pytest.config.getoption('--scale_run'),
                    reason="It can take up to 10 hours to complete")
def test_functional_tests_at_scale(
        get_config, bip_client, prepare_tests, get_scale_size, setup_logging,
        get_scale_long_run):
    """
    BUG:
    Deployment of Application Service fails if N instances were already deployed
    onto BigIP

    This test is a result of misconception that the issues with iStat, MCPD are
    result of number of too many Application Services being deployed on the
    device.
    test_299_load.py is a proof that this assumption is wrong.

    One needs to pass --scale_run flag in order to run this test.
    Bare in mind that combined with --scale_long_run it will take 10+ hours to
    complete.

    In its current form the test generates a lot of logs and kqviews.
    Run with --scale_run --scale_long_run, enabled can produce 30+ GB of logs.
    """

    test_results = {}

    logger = logging.getLogger(__name__)

    log_dir = os.path.join("logs", get_config['session_id'], 'run')
    mk_dir(log_dir)

    for payload_file in get_payload_files(get_config):

        payload_basename = get_payload_basename(payload_file)
        if payload_basename in [
            'test_vs_standard_https_multi_listeners',
            'test_vs_standard_http_ipv6'
        ]:
            logger.warn('Skipping payload {}\n'
                        'Additional modifications are required\n'
                        'to run them at scale.\n'.format(payload_basename))
            # ToDo: add required modifications
            continue

        payload = load_payload(get_config, payload_file)

        first_pool_addr = ipaddress.ip_address(u"172.16.0.100")
        payload_dependencies = get_payload_dependencies(
            prepare_tests, payload_basename)

        test_results[payload['name']] = {
            'scale_size': get_scale_size
        }

        if len(payload_dependencies) > 0 and payload_dependencies[0]['parent']:
            logger.info("Handling dependant scale for {}".format(
                payload_basename))
            dependent_scale(get_config, payload_dependencies, first_pool_addr,
                            bip_client, test_results, log_dir, get_scale_size,
                            get_scale_long_run)

        elif len(payload_dependencies) == 0:
            logger.info("Handling independent scale for {}".format(
                payload_basename))
            independent_scale(
                payload, first_pool_addr, log_dir, bip_client, test_results,
                get_scale_size, get_scale_long_run)

    print(json.dumps(test_results, indent=4, sort_keys=True))

    save_json(os.path.join(log_dir, 'scale_test_result.json'), test_results)

    for payload_name in test_results:
        assert 'deployment_exception' not in test_results[payload_name]
        assert 'removal_exception' not in test_results[payload_name]
