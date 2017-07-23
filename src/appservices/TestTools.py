#!/usr/bin/env python
import json
import os
from glob import glob

import ipaddress

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


def run_functional_tests_at_scale(bip_client, config, app_service_count=10):

    for payload_file in sorted(glob(os.path.join(
            config['payloads_dir'], "*.json"))):
        with open(payload_file, 'r') as payload_file_handle:
            payload = json.load(payload_file_handle)
            if payload["variables"][7]['value'] != "172.16.0.100":
                continue

            if payload['name'] in ['test_vs_standard_https_multi_listeners']:
                # Skipping payload due to:
                # {
                #     "apiError": 3,
                #     "code": 400,
                #     "errorStack": [],
                #     "message": "01070333:3: Virtual Server /Common/test_vs_standard_https_multi_listeners_1.app/test_vs_standard_https_addlisteners_vs_idx_0_445
                # illegally shares destination address, source address, service port, ip-protocol,
                #  and vlan with Virtual Server /Common/test_vs_standard_https_multi_listeners_0.app/test_vs_standard_https_addlisteners_vs_idx_0_445."
                # }
                continue

            pool_addr = ipaddress.ip_address(u"172.16.0.100")

            test_run_log_dir = os.path.abspath(
                os.path.join("logs", config['session_id'],
                             'run', payload['name'])
            )

            try:
                for deployment_no in range(app_service_count):
                    payload['name'] = update_payload_name(
                        payload['name'], deployment_no)
                    payload["variables"][7]['value'] = str(
                        pool_addr+deployment_no)

                    test_run_log_dir = os.path.abspath(
                        os.path.join(
                            "logs", config['session_id'], 'run',
                            strip_payload_name(payload['name']),
                            str(deployment_no))
                    )

                    bip_client.deploy_app_service(payload)
                    bip_client.verify_deployment_result(
                        payload, test_run_log_dir)

                for deployment_no in range(app_service_count):
                    payload['name'] = update_payload_name(
                        payload['name'], deployment_no)
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
