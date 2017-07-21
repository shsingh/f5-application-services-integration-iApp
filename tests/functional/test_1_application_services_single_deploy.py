#!/usr/bin/env python

from src.appservices.TestTools import run_functional_tests


def functional_tests(get_config, bip_client, prepare_tests):
    run_functional_tests(bip_client, get_config)
