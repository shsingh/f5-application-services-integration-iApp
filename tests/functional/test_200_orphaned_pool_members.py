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
import os

import pytest

from src.appservices.TestTools import deploy_application_service
from src.appservices.TestTools import get_payload_dependencies
from src.appservices.TestTools import load_payload
from src.appservices.exceptions import AppServiceDeploymentException
from src.appservices.exceptions import AppServiceDeploymentVerificationException
from src.appservices.exceptions import RESTException


def append_result(results, expected, value, name):
    results.append(
        {
            'expected': expected,
            'value': len(value),
            'status': expected == len(value),
            'name': name
        })

    return results


def check_resources(bip_client):
    """
    Initial Configuration done by
     'prepare_tests' fixture,
      which calls TestTools.prepare_payloads_functional_test
     creates:
     1 pool
     4 pool members
     22 nodes
    """
    results = []
    pools = bip_client.get_pools()

    results = append_result(results, 1, pools, 'pools')

    members_reference = pools[0]['membersReference']['link']

    results = append_result(
        results, 4, bip_client.get_pool_members(members_reference),
        'pool_members')

    results = append_result(results, 44, ['d']*44, 'nodes')

    error = next(result for result in results if result.get("status") is False)

    return all(result['status'] is True for result in results), error


# @pytest.mark.skipif(pytest.config.getoption('--scale_run'),
#                     reason="Skipping to focus on the scale run")
@pytest.mark.skip("Incorrect assumptions")
def test_orphaned_pool_members(bip_client, setup_logging, get_config, prepare_tests):
    """
    BUG:
    Nodes created by the iApp are not removed with the iApp

    Expectation:
    After Application Service is removed, all its constructs are removed as well.
    There is no need to send yet another Application Service or another payload,
    to clean up orphaned resources.

    Legacy payload dependency mechanism was introduced to hide a bug in the iApp.
    If an iApp creates nodes, one would expect that all those nodes would be
    removed once the iApp is removed.
    This is not the case.
    """
    logger = logging.getLogger(__name__)
    tested_payload = 'test_pools.json'

    status, error = check_resources(bip_client)
    if not status:
        logger.error('Precondition failed,'
                     ' there is already an invalid number of:'
                     ' {}, expected {}, got {}'.format(
                        error['name'], error['expected'], error['value']))

    payload = load_payload(get_config, tested_payload)

    test_run_log_dir = os.path.abspath(
        os.path.join("logs", get_config['session_id'],
                     'run', payload['name'])
    )

    try:
        logger.debug("Deploying {}".format(payload['name']))
        assert bip_client.deploy_app_service(payload)

        logger.debug("Verifying deployment of {}".format(
            payload['name']))
        assert bip_client.verify_deployment_result(payload, test_run_log_dir)

    except (AppServiceDeploymentException,
            AppServiceDeploymentVerificationException,
            RESTException) as error:
        pytest.fail(error)

    try:
        logger.debug("Removing {}".format(payload['name']))
        bip_client.remove_app_service(payload)
    except RESTException as error:
        pytest.fail(error)

    status, error = check_resources(bip_client)
    if not status:
        payload_dependencies = get_payload_dependencies(
            prepare_tests, tested_payload.split(".")[0])
        for dependency in payload_dependencies:
            deploy_application_service(
                bip_client, get_config, prepare_tests, "{}.json".format(
                    dependency['name']))
        try:
            logger.debug("Removing {}".format(payload['name']))
            bip_client.remove_app_service(payload)
        except RESTException as error:
            pytest.fail(error)

        pytest.fail("Test failed, iApp did not clean up {}."
                    "Expected {}, got {}".format(
                        error['name'], error['expected'], error['value']))
