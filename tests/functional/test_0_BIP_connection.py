#!/usr/bin/env python

import re

import pytest

from src.appservices.tools import get_timestamp


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
