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
import json

import pytest

from src.appservices.TestTools import load_payload
from src.appservices.exceptions import AppServiceDeploymentException
from src.appservices.exceptions import RESTException
from src.appservices.exceptions import AppServiceDeploymentVerificationException


def check_orphaned_pools(bip_client, logger):
    pools = bip_client.get_pools()

    assert len(pools) == 1

    # if len(pools) > 1:
    #     for pool in pools:
    #         if pool['selfLink'] != 'https://localhost/mgmt/tm/ltm/pool/~Common~test_pool?ver=12.1.1':
    #             logger.warn("Orphaned pool ?, removing...")
    #             logger.debug("Removing {}".format(pool['selfLink']))
    #             bip_client.remove_pool(pool['selfLink'])
    #
    #     pools = bip_client.get_pools()
    #     if len(pools) > 1:
    #         pytest.fail("Failed to remove orphaned pool members")


def check_orphaned_pool_members(bip_client, logger):
    pools = bip_client.get_pools()
    members_reference = pools[0]['membersReference']['link']

    logger.debug("members_reference link: {}".format(members_reference))
    pool_members = bip_client.get_pool_members(members_reference)

    assert len(pool_members) == 4


@pytest.mark.skipif(pytest.config.getoption('--scale_run'),
                    reason="Skipping to focus on the scale run")
def test_orphaned_pool_members(bip_client, setup_logging, get_config, prepare_tests):
    logger = logging.getLogger(__name__)

    check_orphaned_pool_members(bip_client, logger)

    check_orphaned_pools(bip_client, logger)

    payload = load_payload(get_config, 'test_pools.json')

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

    check_orphaned_pool_members(bip_client, logger)

    check_orphaned_pools(bip_client, logger)


    #
    # pool_members = bip_client.get_pool_members()
    # assert len(pool_members) <= 1
