#!/usr/bin/env python

import pytest
import os
from src.appservices.TestTools import prepare_payloads_functional_test
from src.appservices.tools import get_timestamp


@pytest.fixture(scope='module')
def build_payloads():

    session_id = get_timestamp()

    prepare_payloads_functional_test(
        session_id, "10.145.64.120", "10.144.72.137")

    yield
    print("\n!!!cleanup!!!")


def test_hello_world(build_payloads):
    print("hello from test case")
    assert True is True
