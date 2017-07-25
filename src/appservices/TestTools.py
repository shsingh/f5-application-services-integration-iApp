#!/usr/bin/env python
import json
import logging
import os
import threading
from glob import glob

from src.appservices.PayloadGenerator import PayloadGenerator
from src.appservices.exceptions import AppServiceDeploymentException
from src.appservices.exceptions import AppServiceDeploymentVerificationException
from src.appservices.exceptions import AppServiceRemovalException
from src.appservices.exceptions import RESTException
from src.appservices.tools import get_timestamp


def prepare_payloads_functional_test(bip, config):

    bip.upload_files(
            ['resources/test_config.conf'],
            ['/var/tmp/test_config.conf']
        )

    bip.run_command('tmsh -c \"delete ltm pool all;'
                    ' delete ltm node all\"')

    bip.run_command('tmsh load sys config file /var/tmp/test_config.conf merge')

    pay_gen = PayloadGenerator(
        os.getcwd(),
        config['payloads_dir'],
        config['tmp_dir'],
        config['flat_templates_dir']
    )

    version = bip.get_version()

    for payload_template in glob(os.path.join("payload_templates", "*.tmpl")):
        pay_gen.fill_template(
            payload_template, version, config['policy_host'],
            u"172.16.0.0/24",
            u"2001:dead:beef:1::/120",
            u"172.16.0.100",
            u"2001:dead:beef:1::10",
            u"10.0.0.0/24",
            u"2001:dead:beef:2::/120",
            u"10.0.0.10",
            u"2001:dead:beef:2::10")

    for payload_template in glob(os.path.join(config['tmp_dir'], "*.tmpl")):
        pay_gen.build_template(
            config['tmp_dir'],
            payload_template,
            'admin',
            'admin'
        )

    app_service_template_name = bip.get_template_name()

    for payload_template in glob(os.path.join(
            config['flat_templates_dir'], "*.tmpl")):
        pay_gen.build_bip_payload(payload_template, app_service_template_name)


def get_test_config(host, policy_host, test_method='pytest'):
    timestamp = get_timestamp()
    session_id = "{}_{}".format(test_method, timestamp)
    config = {
        'timestamp': timestamp,
        'payloads_dir': os.path.abspath(
            os.path.join("logs", session_id, 'payloads')),
        'tmp_dir': os.path.abspath(os.path.join("logs", session_id, 'tmp')),
        'flat_templates_dir': os.path.abspath(os.path.join(
            "logs", session_id, 'payload_templates')),
        'host': host,
        'policy_host': policy_host,
        'session_id': session_id
    }
    return config


def run_functional_tests(bip_client, config):

    for payload_file in sorted(glob(os.path.join(
            config['payloads_dir'], "*.json"))):
        with open(payload_file, 'r') as payload_file_handle:
            payload = json.load(payload_file_handle)

            test_run_log_dir = os.path.abspath(
                os.path.join("logs", config['session_id'],
                             'run', payload['name'])
            )

            try:
                bip_client.deploy_app_service(payload)

                bip_client.verify_deployment_result(payload, test_run_log_dir)

                bip_client.remove_app_service(payload)
            except AppServiceDeploymentException:
                bip_client.download_logs(test_run_log_dir)
                raise
            except RESTException:
                bip_client.download_logs(test_run_log_dir)
                raise
            except AppServiceDeploymentVerificationException:
                bip_client.download_logs(test_run_log_dir)
                raise
            except AppServiceRemovalException:
                bip_client.download_logs(test_run_log_dir)
                raise


def update_payload_name(name, run):
    name_split = name.split("_")
    try:
        int(name_split[-1])
        name_split[-1] = str(run)
        return "_".join(name_split)
    except ValueError:
        return "{}_{}".format(name, run)


def strip_payload_name(name):
    name_split = name.split("_")
    try:
        int(name_split[-1])
        return "_".join(name_split[:-1])
    except ValueError:
        return name


def load_payload(payload_dir, filename='test_monitors.json'):
    with open(os.path.join(payload_dir, filename)) as payload:
        data = json.load(payload)
    return data


class IappWorker(threading.Thread):
    def __init__(self, bip_client, payload, log_dir, results, thread_no):
        threading.Thread.__init__(self)
        self.bip_client = bip_client
        self.payload = payload
        self.log_dir = log_dir
        self.results = results
        self.thread_no = thread_no
        self.logger = logging.getLogger(__name__)

    def run(self):
        try:
            self.bip_client.deploy_app_service(self.payload)
            self.results[self.thread_no] = {
                'result': True,
                'msg': ''
            }

        except (RESTException, AppServiceDeploymentException) as ex:
            self.bip_client.download_logs(self.log_dir)
            self.results[self.thread_no] = {
                'result': False,
                'msg': ex
            }

        finally:
            return self.results
