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

import argparse
import sys

from src.appservices.BIPClient import BIPClient
from src.appservices.TestTools import get_test_config
from src.appservices.TestTools import prepare_payloads_functional_test
from src.appservices.TestTools import run_legacy_functional_tests
from src.appservices.tools import setup_logging


def run_legacy_test_suite(
        host, policy_host, username, password, no_delete, run_count, retries,
        ignore, ssh_username, ssh_password,  start, end, ssh_port, vs_subnet,
        vs_first_address, vs_v6_subnet, vs_v6_first_address, member_subnet,
        member_first_address, member_v6_subnet, member_v6_first_address):

    bip = BIPClient(
        host, ssh_port=ssh_port, username=username, password=password,
        ssh_username=ssh_username, ssh_password=ssh_password)

    config = get_test_config(
        host, policy_host, no_delete, run_count, retries, ignore, start,
        end, vs_subnet, vs_first_address, vs_v6_subnet, vs_v6_first_address,
        member_subnet, member_first_address, member_v6_subnet,
        member_v6_first_address, "manual")

    delete_overrides = prepare_payloads_functional_test(bip, config)
    run_legacy_functional_tests(bip, config, delete_overrides)


def get_parser():
    parser = argparse.ArgumentParser(
        description='Tool to run appsvcs_integration_iapp legacy test suite')
    parser.add_argument("host",
                        help="The IP/Hostname of the target BIG-IP device")
    parser.add_argument("policy_host",
                        help="The host to use for URL based bundled items")

    parser.add_argument("-u", "--username",
                        help="The BIG-IP username",
                        default="admin")
    parser.add_argument("-p", "--password",
                        help="The BIG-IP password",
                        default="admin")
    parser.add_argument("-n", "--no_delete",
                        help="Don't delete deployments automatically",
                        action="store_true",
                        default=False)
    parser.add_argument("-c", "--run_count",
                        help="The number of times to run tests",
                        type=int,
                        default=1)
    parser.add_argument("-r", "--retries",
                        help="The number of times to retry tests upon failure",
                        type=int,
                        default=1)
    parser.add_argument("-i", "--ignore",
                        help="Comma seperated list of test numbers to ignore/skip",
                        default="")

    parser.add_argument("--ssh_username",
                        help="The BIG-IP ssh username",
                        default="root")
    parser.add_argument("--ssh_password",
                        help="The BIG-IP ssh password",
                        default="default")
    parser.add_argument("--start",
                        help="Test number to start at",
                        type=int,
                        default="0")
    parser.add_argument("--end",
                        help="Test number to end at",
                        type=int,
                        default="-1")
    parser.add_argument("--ssh_port",
                        help="Non default SSH port",
                        type=int,
                        default=22)

    parser.add_argument("--vs_subnet",
                        help="The IPv4 subnet for Virtual Server IPs",
                        default="172.16.0.0/24")
    parser.add_argument("--vs_first_address",
                        help="The first IPv4 Virtual Server IP",
                        default="172.16.0.100")
    parser.add_argument("--vs_v6_subnet",
                        help="The IPv6 subnet for Virtual Server IPs",
                        default="2001:dead:beef:1::/120")
    parser.add_argument("--vs_v6_first_address",
                        help="The first IPv6 Virtual Server IP",
                        default="2001:dead:beef:1::10")
    parser.add_argument("--member_subnet",
                        help="The IPv4 subnet for Pool Member IPs",
                        default="10.0.0.0/24")
    parser.add_argument("--member_first_address",
                        help="The first IPv4 Pool Member IP",
                        default="10.0.0.10")
    parser.add_argument("--member_v6_subnet",
                        help="The first IPv6 Pool Member IP",
                        default="2001:dead:beef:2::/120")
    parser.add_argument("--member_v6_first_address",
                        help="The IPv6 subnet for Pool Member IPs",
                        default="2001:dead:beef:2::10")

    return parser


def router(parser, argv):
    if len(argv) < 2:
        parser.print_help()
        sys.exit(1)

    args = parser.parse_args()

    setup_logging()

    if args.host and args.policy_host:
        run_legacy_test_suite(
            args.host, args.policy_host, args.username, args.password,
            args.no_delete, args.run_count, args.retries, args.ignore,
            args.ssh_username, args.ssh_password, args.start, args.end,
            args.ssh_port, args.vs_subnet, args.vs_first_address,
            args.vs_v6_subnet, args.vs_v6_first_address, args.member_subnet,
            args.member_first_address, args.member_v6_subnet,
            args.member_v6_first_address)


if __name__ == "__main__":
    parser = get_parser()
    router(parser, sys.argv)
