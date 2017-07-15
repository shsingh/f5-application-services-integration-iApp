#!/usr/bin/env python

import pytest
import AppServicesTools as at


def test_ip_v4_address_generator():
    addr_gen = at.IPv4AddressGenerator(u"10.0.0.0/24")
    assert str(addr_gen.get_next()) == "10.0.0.1"
    assert str(addr_gen.get_next()) == "10.0.0.2"
    assert str(addr_gen.get_next()) == "10.0.0.3"

    assert str(addr_gen.get_last()) == "10.0.0.254"
    assert str(addr_gen.get_last()) == "10.0.0.253"
    assert str(addr_gen.get_last()) == "10.0.0.252"

    assert str(addr_gen.get_network_address()) == "10.0.0.0"


def test_ip_v6_address_generator():
    addr_gen = at.IPv6AddressGenerator(u"2001:dead:beef:2::/120")
    assert str(addr_gen.get_next()) == "2001:dead:beef:2::1"
    assert str(addr_gen.get_next()) == "2001:dead:beef:2::2"
    assert str(addr_gen.get_next()) == "2001:dead:beef:2::3"

    assert str(addr_gen.get_network_address()) == "2001:dead:beef:2::"