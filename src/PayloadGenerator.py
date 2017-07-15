#!/usr/bin/env python

import os
import re
import random
from AppServicesTools import IPv4AddressGenerator, IPv6AddressGenerator


class PayloadGenerator(object):
    def __init__(self,
                 base_dir,
                 template_dir='templates',
                 payloads_dir='payloads',
                 tmp_dir='tmp'):
        self._base_dir = os.path.abspath(base_dir)
        self._template_dir = os.path.abspath(template_dir)
        self._payloads_dir = os.path.abspath(payloads_dir)
        self._tmp_dir = os.path.abspath(tmp_dir)

    def build_template(self, file_name, session_id, version, policy_host,
                       pull_v4_network, pull_v6_network):

        v4_gen = IPv4AddressGenerator(pull_v4_network)
        v6_gen = IPv6AddressGenerator(pull_v6_network)

        result = list(False, "", "Common")
        
        with open(file_name) as template:
            with open(os.path.join(
                self._tmp_dir,
                "{}_{}.tmp".format(file_name, session_id)
            ), "wt") as tmp:
                for line in template:
                    line = re.sub(
                        r'\%TEST_NAME\%', file_name.split('.')[0], line)
                    vs_ip_match = re.match(
                        r'.*%TEST_VS_IP%.*', line)
                    vs6_ip_match = re.match(
                        r'.*%TEST_VS6_IP%.*', line)
                    member_ip_match = re.match(
                        r'.*%TEST_MEMBER_IP%.*', line)
                    member6_ip_match = re.match(
                        r'.*%TEST_MEMBER6_IP%.*', line)
                    snat_ip_match = re.match(
                        r'.*%TEST_RANGE_(\d)_IP%.*', line)
                    snat6_ip_match = re.match(
                        r'.*%TEST_RANGE6_(\d)_IP%.*', line)
                    version_match = re.match(
                        r'.*%TEST_DEV_VERSION_(.*)%.*', line)
                    delete_override_match = re.match(
                        r'.*\"test_delete_override\":\"true\".*', line)
                    parent_match = re.match(
                        r'.*\"test_parent\":\"(.*)\".*', line)
                    partition_match = re.match(
                        r'.*\"partition\":\"(.*)\".*', line)
                    policyhost_match = re.match(
                        r'.*%TEST_POLICY_HOST%.*', line)
                    random_match = re.match(
                        r'.*%RANDOM%.*', line)

                    if random_match:
                        line = re.sub(
                            r'\%RANDOM\%',
                            str(random.randint(10000, 99999)), line)

                    if partition_match:
                        result[2] = partition_match.group(1)

                    if parent_match:
                        result[1] = parent_match.group(1)

                    if policyhost_match:
                        line = re.sub(r'\%TEST_POLICY_HOST\%',
                                      policy_host, line)

                    if delete_override_match:
                        result[0] = True

                    if version_match:
                        if version_match.group(1) == "MAJOR":
                            line = re.sub(r'\%TEST_DEV_VERSION_MAJOR\%',
                                          version["major"], line)

                        if version_match.group(1) == "MINOR":
                            line = re.sub(r'\%TEST_DEV_VERSION_MINOR\%',
                                          version["minor"], line)

                        if version_match.group(1) == "FULL":
                            line = re.sub(r'\%TEST_DEV_VERSION_FULL\%',
                                          version["version"], line)

                    if vs_ip_match:
                        line = re.sub(r'\%TEST_VS_IP\%',
                                      "{}".format(
                                          v4_gen.get_next()), line)

                    if vs6_ip_match:
                        line = re.sub(r'\%TEST_VS6_IP\%',
                                      "{}".format(
                                          v6_gen.get_next()), line)

                    if member_ip_match:
                        line = re.sub(r'\%TEST_MEMBER_IP\%',
                                      "{}".format(
                                          v4_gen.get_next()
                                      ), line)

                    if member6_ip_match:
                        line = re.sub(r'\%TEST_MEMBER6_IP\%',
                                      "{}".format(
                                          v6_gen.get_next()), line)

                    if snat_ip_match:
                        snat_ips = []
                        for sip in range(int(snat_ip_match.group(1))):
                            snat_ips.append(v4_gen.get_last())
                        line = re.sub(r'\%TEST_RANGE_[\d]_IP\%',
                                      "{}".format(','.join(snat_ips)), line)

                    if snat6_ip_match:
                        snat6_ips = []
                        for s6ip in range(int(snat6_ip_match.group(1))):
                            snat6_ips.append(v6_gen.get_last())
                        line = re.sub(r'\%TEST_RANGE6_[\d]_IP\%',
                                      "{}".format(','.join(snat6_ips)), line)

                    tmp.write(line)

        return result

