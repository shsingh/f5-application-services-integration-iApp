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

import logging
import os
import threading
from Queue import Empty
from Queue import Queue

import ipaddress
import pytest

from src.appservices.BIPClient import BIPClient
from src.appservices.TestTools import load_payload
from src.appservices.TestTools import update_payload_name
from src.appservices.exceptions import AppServiceDeploymentException
from src.appservices.exceptions import AppServiceDeploymentVerificationException
from src.appservices.exceptions import RESTException
from src.appservices.tools import mk_dir


class iStatWorker(threading.Thread):
    def __init__(self, payload_queue, result_queue, logger, host, threads):
        super(iStatWorker, self).__init__()
        self.payload_queue = payload_queue
        self.result_queue = result_queue
        self.stop_request = threading.Event()
        self.logger = logger
        self.threads = threads
        self.bip_client = BIPClient(host, logger=self.logger)

        self.start()

    def run(self):
        while not self.stop_request.isSet():
            try:
                self.process_payload_queue()
            except Empty:
                return

    def join(self, timeout=60):
        self.logger.debug("Joining thread")
        self.stop_request.set()
        super(iStatWorker, self).join(timeout)

    def stop_threads(self):
        for thread in self.threads:
            thread.stop_request.set()

    def process_payload_queue(self):
        payload, log_dir, payload_no = self.payload_queue.get(True, 0.05)
        try:
            self.logger.info("Deploying {}".format(payload['name']))
            app_deployed = self.bip_client.deploy_app_service(
                payload)

            self.logger.info("Verifying deployment of {}".format(
                payload['name']))
            deployment_verified = self.bip_client.verify_deployment_result(
                payload, log_dir)

            self.result_queue.put({
                'payload_no': payload_no,
                'app_deployed': app_deployed,
                'deployment_verified': deployment_verified
            })

        except (RESTException,
                AppServiceDeploymentException,
                AppServiceDeploymentVerificationException) as error:
            self.logger.exception(error)
            self.result_queue.put({
                'payload_no': payload_no,
                'error': error,
                'log_dir': log_dir
            })
            self.stop_threads()


class REST_killer(iStatWorker):
    def __init__(self, payload_queue, result_queue, logger, host, threads):
        iStatWorker.__init__(
            self, payload_queue, result_queue, logger, host, threads)

    def process_payload_queue(self):
        payload, log_dir, payload_no = self.payload_queue.get(True, 0.05)
        try:
            self.logger.info("Deploying {}".format(payload['name']))
            app_deployed = self.bip_client.deploy_app_service(
                payload)

            self.logger.info("Verifying deployment of {}".format(
                payload['name']))
            deployment_verified = self.bip_client.verify_deployment_result(
                payload, log_dir)

            self.result_queue.put({
                'payload_no': payload_no,
                'app_deployed': app_deployed,
                'deployment_verified': deployment_verified
            })

        except (AppServiceDeploymentException,
                AppServiceDeploymentVerificationException) as error:
            self.logger.exception(error)

        except RESTException as error:
            self.logger.critical("lala: {}".format(str(error.get_response())))
            if error.get_response().status_code >= 500:
                self.result_queue.put({
                    'payload_no': payload_no,
                    'error': error,
                    'log_dir': log_dir
                })
                self.stop_threads()


def prepare(payload_count, config):
    threads = []
    payload_queue = Queue()
    result_queue = Queue()

    base_ip_address = ipaddress.ip_address(u'10.10.200.0')
    logger = logging.getLogger(__name__)

    logger.debug("Loading payload_queue")

    for payload_no in range(payload_count):
        payload = load_payload(config, 'test_monitors.json')
        payload['name'] = update_payload_name(payload['name'], payload_no)
        payload["variables"][7]['value'] = str(base_ip_address + payload_no)

        base_log_dir = os.path.abspath(
            os.path.join("logs", config['session_id'],
                         'mcpd_thread'))

        log_dir = os.path.join(base_log_dir, str(payload_no), payload['name'])

        mk_dir(log_dir)

        payload_queue.put((
            payload,
            log_dir,
            payload_no
        ))

    return threads, payload_queue, result_queue, logger, payload, base_log_dir


def remove_empty_folders(path, remove_root=False):
    """
    Function to remove empty folders
    """
    if not os.path.isdir(path):
        return

    # remove empty subfolders
    files = os.listdir(path)
    if len(files):
        for f in files:
            fullpath = os.path.join(path, f)
            if os.path.isdir(fullpath):
                remove_empty_folders(fullpath)

    # if folder empty, delete it
    files = os.listdir(path)
    if len(files) == 0 and remove_root:
        print "Removing empty folder:", path
        os.rmdir(path)


def cleanup(logger, payload_count, payload, host, base_log_dir):
    logger.debug("Removing Application services...")
    for payload_no in range(payload_count):
        payload['name'] = update_payload_name(payload['name'], payload_no)
        logger.debug("Removing {}".format(payload['name']))
        bip_client = BIPClient(host)
        bip_client.remove_app_service(payload)

    remove_empty_folders(base_log_dir)


def download_logs(host, logger, payload_count, result_queue):
    bip_client = BIPClient(host, logger=logger)
    for payload_no in range(payload_count):
        try:
            result = result_queue.get(True, 60)
        except Empty:
            continue

        logger.debug("Getting result from {}".format(result['payload_no']))

        if 'error' in result:
            logger.error("Exception in result_queue: {},"
                         "downloading logs...".format(result))
            bip_client.download_logs(result['log_dir'])
            bip_client.download_qkview(result['log_dir'])
            pytest.fail(
                "Exception in result_queue, test failed: {}".format(result))
            break


@pytest.mark.skipif(pytest.config.getoption('--scale_run'),
                    reason="Skipping to focus on the scale run")
def test_iStat_response(get_config, get_host, prepare_tests, setup_logging,
                          payload_count=50, worker_count=10):

    threads, payload_queue, result_queue, logger, payload, base_log_dir = prepare(
        payload_count, get_config)

    for worker_no in range(worker_count):
        threads.append(iStatWorker(
            payload_queue, result_queue, logger, get_host, threads))

    download_logs(get_host, logger, payload_count, result_queue)

    for thread in threads:
        thread.join()

    cleanup(logger, payload_count, payload, get_host, base_log_dir)


@pytest.mark.skipif(pytest.config.getoption('--scale_run'),
                    reason="Skipping to focus on the scale run")
def test_kill_control_plane(get_config, get_host, prepare_tests, setup_logging,
                        payload_count=50, worker_count=10):

    threads, payload_queue, result_queue, logger, payload, base_log_dir = prepare(
        payload_count, get_config)

    for worker_no in range(worker_count):
        threads.append(REST_killer(
            payload_queue, result_queue, logger, get_host, threads))

    download_logs(get_host, logger, payload_count, result_queue)

    for thread in threads:
        thread.join()

    cleanup(logger, payload_count, payload, get_host, base_log_dir)
