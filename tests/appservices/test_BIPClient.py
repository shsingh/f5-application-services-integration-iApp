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

import pytest

from src.appservices.BIPClient import BIPClient
from src.appservices.exceptions import RESTException


class MockedResponse(object):
    def __init__(self, status_code):
        self._status_code = status_code

    @property
    def status_code(self):
        return self._status_code

    @status_code.setter
    def status_code(self, status_code):
        self._status_code = status_code

    def json(self):
        return {}


def test_handle_response(setup_logging):
    logger = logging.getLogger(__name__)
    bip_client = BIPClient("127.0.0.1")

    response_200 = MockedResponse(200)

    assert bip_client.handle_response(response_200) == {}
    assert bip_client.handle_response(response_200) is not False

    response_400 = MockedResponse(404)

    assert bip_client.handle_response(response_400) is False

    response_500 = MockedResponse(500)

    with pytest.raises(RESTException):
        bip_client.handle_response(response_500)
