#!/usr/bin/env python

import pytest
import re
import os
import json
from glob import glob
from src.appservices.TestTools import prepare_payloads_functional_test
from src.appservices.tools import get_timestamp
from src.appservices.BIPClient import BIPClient


@pytest.fixture(scope='module')
def build_payloads():

    timestamp = get_timestamp()
    session_id = "pytest_{}".format(timestamp)
    config = {
        'timestamp': get_timestamp(),
        'payloads_dir': os.path.abspath(
            os.path.join("logs", session_id, 'payloads')),
        'tmp_dir': os.path.abspath(os.path.join("logs", session_id, 'tmp')),
        'flat_templates_dir': os.path.abspath(os.path.join(
            "logs", session_id, 'payload_templates')),
        'host': "10.145.64.120",
        'policy_host': "10.144.72.137"
    }

    prepare_payloads_functional_test(config)

    return config


@pytest.fixture(scope='module')
def bip_client():
    return BIPClient("10.145.64.120")


@pytest.mark.order1
def test_https_credentials(bip_client):
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


@pytest.mark.order2
def test_ssh_credentials(bip_client):
    stdout = bip_client.run_command("date +%s")
    match = re.match(r'(\d)', stdout)

    assert match.group(0)


@pytest.mark.order3
def test_time_delta_less_than_ten_seconds(bip_client):
    bip_time = int(bip_client.run_command("date +%s"))
    local_time = get_timestamp()

    assert (local_time - bip_time) < 10


@pytest.mark.order4
def test_payloads(build_payloads, bip_client):
    for payload_file in sorted(glob(os.path.join(
            build_payloads['payloads_dir'], "*.json"))):
        with open(payload_file, 'r') as payload_file_handle:
            payload = json.load(payload_file_handle)

            assert bip_client.deploy_app_service(payload)
            assert bip_client.remove_app_service(payload)
