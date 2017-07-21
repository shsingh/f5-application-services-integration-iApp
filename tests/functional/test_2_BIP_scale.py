#!/usr/bin/env python

import pytest

from src.appservices.TestTools import run_functional_tests_at_scale


@pytest.mark.skip(reason="Skipping just for fun of it")
def functional_tests_at_scale(
        get_config, bip_client, prepare_tests, scale_size):
    run_functional_tests_at_scale(bip_client, get_config, scale_size)
