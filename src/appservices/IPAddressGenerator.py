#!/usr/bin/env python

import ipaddress


class IPAddressGenerator(object):
    def __init__(self, network, first_address_str):
        self._network = network
        self._hosts = []
        first_address = ipaddress.ip_address(first_address_str)

        trigger = False
        for address in list(self._network.hosts()):
            if address == first_address:
                trigger = True
            if trigger:
                self._hosts.append(address)

        self._hosts = list(reversed(self._hosts))

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
    def __init__(self, network_str, first_address_str):
        super(IPv4AddressGenerator, self).__init__(
            ipaddress.IPv4Network(network_str), first_address_str)


class IPv6AddressGenerator(IPAddressGenerator):
    def __init__(self, network_str, first_address_str):
        super(IPv6AddressGenerator, self).__init__(
            ipaddress.IPv6Network(network_str), first_address_str)
