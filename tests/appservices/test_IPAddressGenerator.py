#!/usr/bin/env python
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
