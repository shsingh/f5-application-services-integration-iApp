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

import json
import logging
import os
import threading

import ipaddress
import pytest
from Queue import Queue

from src.appservices.BIPClient import BIPClient
from src.appservices.TestTools import load_payload
from src.appservices.TestTools import update_payload_name
from src.appservices.exceptions import AppServiceDeploymentException
from src.appservices.exceptions import RESTException
from src.appservices.tools import mk_dir


class IappWorker(threading.Thread):
    def __init__(self, host, payload, log_dir, results, thread_no):
        threading.Thread.__init__(self)
        self.daemon = True
        self.log_dir = log_dir

        self.logger = logging.getLogger(__name__)
        file_handler = logging.FileHandler(os.path.join(
            self.log_dir, "thread.log"))
        formatter = logging.Formatter(
            'T{} %(asctime)s - %(name)s - %(levelname)s - %(message)s'.format(
                thread_no))
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

        self.bip_client = BIPClient(host, logger=self.logger)

        self.payload = payload
        self.results = results
        self.thread_no = thread_no

        self.logger.info("Initiating thread {}".format(thread_no))
        self.start()

    def run(self):
        self.logger.info("Running thread {}".format(
            threading.current_thread().getName()))
        try:
            self.results[self.thread_no] = {
                'app_deployed': self.bip_client.deploy_app_service(
                    self.payload),
                'deployment_verified': self.bip_client.verify_deployment_result(
                    self.payload, self.log_dir),
                'msg': '',
                'result': True,
            }

        except (RESTException, AppServiceDeploymentException) as ex:
            # self.bip_client.download_logs(self.log_dir)
            self.logger.exception(ex)
            self.results[self.thread_no] = {
                'result': False,
                'msg': str(ex)
            }


@pytest.mark.skipif(pytest.config.getoption('--scale_run'),
                    reason="Skipping to focus on the scale run")
def test_MCPD_load_issues(
        get_config, get_host, prepare_tests, setup_logging, thread_count=10):
    threads = []
    results = {}
    base_ip_address = ipaddress.ip_address(u'10.10.200.0')
    logger = logging.getLogger(__name__)

    logger.debug("Running threads...")
    for thread_no in range(thread_count):

        payload = load_payload(get_config, 'test_monitors.json')
        payload['name'] = update_payload_name(payload['name'], thread_no)

        payload["variables"][7]['value'] = str(base_ip_address + thread_no)

        log_dir = os.path.abspath(
            os.path.join("logs", get_config['session_id'],
                         'mcpd_thread', str(thread_no), payload['name'])
        )

        mk_dir(log_dir)

        threads.append(IappWorker(
            get_host, payload, log_dir, results, thread_no))

    logger.debug("Joining threads...")
    for thread in threads:
        thread.join()

    with open("thread_run.json", 'w') as out:
        json.dump(results, out, indent=4)

    logger.debug("Removing Application services...")
    for thread_no in range(thread_count):
        payload['name'] = update_payload_name(payload['name'], thread_no)
        logger.debug("Removing {}".format(payload['name']))
        bip_client = BIPClient(get_host)
        bip_client.remove_app_service(payload)
