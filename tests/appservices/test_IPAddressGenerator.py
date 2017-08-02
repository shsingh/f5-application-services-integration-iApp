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
from src.appservices.IPAddressGenerator import IPv4AddressGenerator
from src.appservices.IPAddressGenerator import IPv6AddressGenerator


def test_ip_v4_address_generator():
    addr_gen = IPv4AddressGenerator(u"10.0.0.0/24", u'10.0.0.10')
    assert str(addr_gen.get_next()) == "10.0.0.10"
    assert str(addr_gen.get_next()) == "10.0.0.11"
    assert str(addr_gen.get_next()) == "10.0.0.12"

    assert str(addr_gen.get_last()) == "10.0.0.254"
    assert str(addr_gen.get_last()) == "10.0.0.253"
    assert str(addr_gen.get_last()) == "10.0.0.252"

    assert str(addr_gen.get_network_address()) == "10.0.0.0"


def test_ip_v6_address_generator():
    addr_gen = IPv6AddressGenerator(u"2001:dead:beef:2::/120",
                                          u"2001:dead:beef:2::10")
    assert str(addr_gen.get_next()) == "2001:dead:beef:2::10"
    assert str(addr_gen.get_next()) == "2001:dead:beef:2::11"
    assert str(addr_gen.get_next()) == "2001:dead:beef:2::12"

    assert str(addr_gen.get_network_address()) == "2001:dead:beef:2::"
