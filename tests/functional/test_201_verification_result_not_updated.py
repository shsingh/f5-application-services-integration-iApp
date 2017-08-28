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

from src.appservices.TestTools import get_payload_basename
from src.appservices.TestTools import get_payload_files
from src.appservices.TestTools import load_payload
from src.appservices.TestTools import handle_configuration_payload
from src.appservices.TestTools import get_payload_dependencies


@pytest.mark.skipif(pytest.config.getoption('--scale_run'),
                    reason="Skipping to focus on the scale run")
def test_verification_result_not_updated(
        get_config, get_host, prepare_tests, bip_client, setup_logging):
    """
    After deployment of
    test_vs_standard_https_bundle_all_preserve
    deployment of
    test_vs_standard_https_bundle_all_preserve_2
    follows as a result of obsolete 'payload dependency mechanism'

    It looks like there is a bug on BigIP 11.6.1, which results in failure in
    deployment verification of an update:
    test_vs_standard_https_bundle_all_preserve_2
    """

    get_config['start'] = 26
    get_config['end'] = 28

    payload_files = get_payload_files(get_config)

    assert len(payload_files) == 2

    for payload_file in payload_files:

        payload = load_payload(get_config, payload_file)
        payload_basename = get_payload_basename(payload_file)

        payload_dependencies = get_payload_dependencies(
            prepare_tests, payload_basename)

        assert payload_basename in [
            'test_vs_standard_https_bundle_all_preserve',
            'test_vs_standard_https_bundle_all_preserve_2']

        test_run_log_dir = os.path.abspath(
            os.path.join("logs", get_config['session_id'],
                         'run', payload['name'])
        )

        try:
            handle_configuration_payload(get_config, bip_client, payload_basename, payload,
                                         test_run_log_dir, payload_dependencies)
        except Exception as ex:
            logger = logging.getLogger(__name__)
            logger.exception(ex)
            pytest.fail("Exception raised, test failed")
