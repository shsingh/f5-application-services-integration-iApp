#!/usr/bin/env python

from src.appservices.TestTools import run_functional_tests_at_scale


def test_functional_tests_at_scale(
        get_config, bip_client, prepare_tests, get_scale_size):
    run_functional_tests_at_scale(bip_client, get_config, get_scale_size)
