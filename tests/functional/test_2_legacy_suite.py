#!/usr/bin/env python

import pytest

from src.appservices.TestTools import run_legacy_functional_tests


# @pytest.mark.skip(reason="Skipping in order to focus on scale")
def test_functional_tests(get_config, bip_client, prepare_tests):
    run_legacy_functional_tests(bip_client, get_config, prepare_tests)
