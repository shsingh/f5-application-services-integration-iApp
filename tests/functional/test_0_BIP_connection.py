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

import os
import re

import pytest

from src.appservices.tools import get_timestamp
from src.appservices.tools import mk_dir


@pytest.mark.order(1)
def test_https_credentials(setup_logging, bip_client):
    try:
        version = bip_client.get_version()
    except:
        pytest.fail("Incorrect https credentials")

    assert 'version' in version
    assert version['version'] != ''
    assert 'minor' in version
    assert version['minor'] != ''
    assert 'major' in version
    assert version['major'] != ''


@pytest.mark.order(2)
def test_ssh_credentials(bip_client):
    stdout, _ = bip_client.run_command("date +%s")
    match = re.match(r'(\d)', stdout)

    assert match.group(0)


@pytest.mark.order(3)
def test_time_delta_less_than_ten_seconds(bip_client):
    stdout, _ = bip_client.run_command("date +%s")
    bip_time = int(stdout)
    local_time = get_timestamp()

    assert (local_time - bip_time) < 10


@pytest.mark.skip(reason="Skipping just for fun of it")
def skipped_test():
    pass


@pytest.mark.order(4)
def test_download_reference_qkview(get_config, bip_client):
    log_dir = os.path.join("logs", get_config['session_id'], 'run')
    mk_dir(log_dir)
    filename = bip_client.download_qkview(log_dir)
    assert os.path.isfile(os.path.join(log_dir, filename))
