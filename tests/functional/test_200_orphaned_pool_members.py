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

import pytest


@pytest.mark.skipif(pytest.config.getoption('--scale_run'),
                    reason="Skipping to focus on the scale run")
def test_orphaned_pool_members(bip_client, setup_logging, get_config):
    """
    BUG:
    Pool is created with a pool member
    Pool is removed, node is orphaned.

    Expectation:
    After removal of a pool, all its pool members are also removed

    Legacy payload dependency mechanism was implemented in the iApp test runner
    to hide a bug in BigIP REST.
    If an iApp creates pool with members and afterwards this iApp is deleted.
    One would expect for the created pool and pool members to be removed as well
    """
    logger = logging.getLogger(__name__)

    box_name = "just-a-box:443"

    members = [{
        "name": box_name,
        "address": "10.0.0.1"
    }]

    pool_of_dismay = 'pool_of_dismay'

    bip_client.create_pool(pool_of_dismay, members)

    pool_ok = False
    pool_link = ''
    pools = bip_client.get_pools()
    for pool in pools:
        if pool['name'] == pool_of_dismay:
            pool_link = pool['selfLink']
            pool_members_url = pool['membersReference']['link']
            members = bip_client.get_pool_members(pool_members_url)
            for member in members:
                print(member)
                if member['name'] == box_name:
                    pool_ok = True
                    break

    assert pool_ok
    logger.debug("Pool successively created")

    bip_client.remove_pool(pool_link)

    nodes = bip_client.get_nodes()
    for node in nodes:
        if node['name'] == 'just-a-box':

            node_url = node['selfLink']

            bip_client.rest_delete(node_url)
            pytest.fail("Node {} was not removed after removal of a pool"
                        " that created it".format(node_url))
