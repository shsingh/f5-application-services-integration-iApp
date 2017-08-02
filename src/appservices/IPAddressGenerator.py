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
            ipaddress.IPv4Network(
                unicode(network_str)), unicode(first_address_str))


class IPv6AddressGenerator(IPAddressGenerator):
    def __init__(self, network_str, first_address_str):
        super(IPv6AddressGenerator, self).__init__(
            ipaddress.IPv6Network(
                unicode(network_str)), unicode(first_address_str))
