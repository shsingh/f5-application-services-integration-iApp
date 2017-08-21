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

import pytest
import logging

from src.appservices.TestTools import run_legacy_functional_tests


@pytest.mark.skipif(pytest.config.getoption('--scale_run'),
                    reason="Skipping to focus on the scale run")
def test_functional_tests(get_config, bip_client, prepare_tests, setup_logging):
    """
    This test (compared to original) has modified default value for
     repeating the deployment of an (configuration payload/application service)
     in case of failure.
    Currently only one attempt is made to deploy the payload.
    The original was trying 3 times.

    This is how the application was tested before the pytest.
    (configuration payload/application service) was simply POSTed to BigIP
    and then script verified if that deployment succeeded or not. If not, two
    more attempts were made (3 in total). If any of them succeeded then
    the 'test' was marked as success.

    Originally the test verified the 'happy path' and was made to show that the
    solution works.
    It did the job by hiding numerous underlining BigIP bugs.

    (configuration payloads/application services) are constructed from
    payload templates once can find in the payload_templates folder in the root
    of the project.
    """
    try:
        run_legacy_functional_tests(bip_client, get_config, prepare_tests)
    except Exception as ex:
        logger = logging.getLogger(__name__)
        logger.exception(ex)
        pytest.fail("Exception raised, test failed")
