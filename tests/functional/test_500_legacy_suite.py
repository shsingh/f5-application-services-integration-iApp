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
    try:
        run_legacy_functional_tests(bip_client, get_config, prepare_tests)
    except Exception as ex:
        logger = logging.getLogger(__name__)
        logger.exception(ex)
        pytest.fail("Exception raised, test failed")
