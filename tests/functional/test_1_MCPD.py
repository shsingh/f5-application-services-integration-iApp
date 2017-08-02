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

import os

import ipaddress
import pytest

from src.appservices.BIPClient import BIPClient
from src.appservices.TestTools import IappWorker
from src.appservices.TestTools import load_payload
from src.appservices.TestTools import update_payload_name


@pytest.mark.skip(reason="Skipping because it's not ready")
def test_replicate_mcpd_bug(
        get_config, get_host, prepare_tests, thread_count=5):
    threads = []
    results = {}
    base_ip_address = ipaddress.ip_address(u'10.10.200.0')
    payload = load_payload(get_config['payloads_dir'], 'test_monitors.json')

    for thread_no in range(thread_count):
        payload['name'] = update_payload_name(payload['name'], thread_no)
        log_dir = os.path.abspath(
            os.path.join("logs", get_config['session_id'],
                         'mcpd_thread', payload['name'])
        )

        payload["variables"][7]['value'] = str(base_ip_address + thread_count)

        bip_client = BIPClient(get_host)
        threads.append(IappWorker(
            bip_client, payload, log_dir, results, thread_no))

        threads[-1].daemon = True
        threads[-1].start()

    for thread_no in threads:
        thread_no.join()

    bip_client.download_files([
        '/var/tmp/scriptd.out'
    ], os.path.abspath(
        os.path.join("logs", get_config['session_id'])
    ))

    for thread_no in range(thread_count):
        payload['name'] = update_payload_name(payload['name'], thread_no)
        bip_client.remove_app_service(payload)
