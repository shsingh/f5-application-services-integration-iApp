#!/usr/bin/env python

import re

import pytest

from src.appservices.BIPClient import BIPClient
from src.appservices.TestTools import get_test_config
from src.appservices.TestTools import prepare_payloads_functional_test
from src.appservices.TestTools import run_functional_tests
from src.appservices.tools import get_timestamp


@pytest.fixture(scope='module')
def get_config():
    return get_test_config("10.145.64.120", "10.144.72.137")


@pytest.fixture(scope='module')
def prepare_tests(bip_client, get_config):

    prepare_payloads_functional_test(bip_client, get_config)


@pytest.fixture(scope='module')
def bip_client():
    return BIPClient("10.145.64.120")


@pytest.mark.order(1)
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


@pytest.mark.order(2)
def test_ssh_credentials(bip_client):
    stdout = bip_client.run_command("date +%s")
    match = re.match(r'(\d)', stdout)

    assert match.group(0)


@pytest.mark.order(3)
def test_time_delta_less_than_ten_seconds(bip_client):
    bip_time = int(bip_client.run_command("date +%s"))
    local_time = get_timestamp()

    assert (local_time - bip_time) < 10


@pytest.mark.order(4)
def test_payloads(get_config, bip_client, prepare_tests):
    run_functional_tests(bip_client, get_config)
