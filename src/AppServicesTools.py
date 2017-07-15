#!/usr/bin/env python

import ipaddress


class IPAddressGenerator(object):
    def __init__(self, network):
        self._network = network
        self._hosts = list(reversed(list(self._network.hosts())))

    def get_next(self):
        return self._hosts.pop()

    def get_last(self):
        hosts = list(reversed(self._hosts))
        last = hosts.pop()
        self._hosts = list(reversed(hosts))
        return last

    def get_network_address(self):
        return self._network.network_address


class IPv4AddressGenerator(IPAddressGenerator):
    def __init__(self, network_str):
        super(IPv4AddressGenerator, self).__init__(
            ipaddress.IPv4Network(network_str))


class IPv6AddressGenerator(IPAddressGenerator):
    def __init__(self, network_str):
        super(IPv6AddressGenerator, self).__init__(
            ipaddress.IPv6Network(network_str))
