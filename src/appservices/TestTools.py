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


def prepare_bip(bip):
    bip.upload_files(
        ['resources/test_config.conf'],
        ['/var/tmp/test_config.conf']
    )

    bip.run_command('tmsh -c \"delete ltm pool all;'
                    ' delete ltm node all\"')

    bip.run_command('tmsh load sys config file /var/tmp/test_config.conf merge')

    return bip.get_version(), bip.get_template_name()


def build_application_service_payloads(
        config, version, tcl_template_name="dummy"):

    pay_gen = PayloadGenerator(
        os.getcwd(),
        config['payloads_dir'],
        config['tmp_dir'],
        config['flat_templates_dir']
    )

    for payload_template in glob(os.path.join("payload_templates", "*.tmpl")):
        pay_gen.fill_template(
            payload_template, version, config['policy_host'],
            config['vs_subnet'],
            config['vs_v6_subnet'],
            config['vs_first_address'],
            config['vs_v6_first_address'],
            config['member_subnet'],
            config['member_v6_subnet'],
            config['member_first_address'],
            config['member_v6_first_address'])

    delete_overrides = {}
    for payload_template in glob(os.path.join(config['tmp_dir'], "*.tmpl")):
        pay_gen.build_template(
            config['tmp_dir'],
            payload_template,
            'admin',
            'admin'
        )
        # this is where payload dependencies are resolved
        # can we please remove this and make the payloads independent ?
        template_name = os.path.splitext(os.path.basename(payload_template))[0]

        if pay_gen.check_delete_override(config['tmp_dir'], payload_template):
            delete_overrides[template_name] = True

    for payload_template in glob(os.path.join(
            config['flat_templates_dir'], "*.tmpl")):
        pay_gen.build_bip_payload(payload_template, tcl_template_name)

    return delete_overrides


def prepare_payloads_functional_test(bip, config):
    version, tcl_template_name = prepare_bip(bip)
    return build_application_service_payloads(
        config, version, tcl_template_name)


def get_test_config(
        host, policy_host, no_delete=False, run_count=1, retries=1, ignore="",
        start=0, end=-1,
        vs_subnet="172.16.0.0/24",
        vs_first_address="172.16.0.100",
        vs_v6_subnet="2001:dead:beef:1::/120",
        vs_v6_first_address="2001:dead:beef:1::10",
        member_subnet="10.0.0.0/24",
        member_first_address="10.0.0.10",
        member_v6_subnet="2001:dead:beef:2::/120",
        member_v6_first_address="2001:dead:beef:2::10",
        test_method='pytest'):

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
        'session_id': session_id,
        'no_delete': no_delete,
        'run_count': run_count,
        'retries': retries,
        'ignore': ignore,
        'start': start,
        'end': end,
        'vs_subnet': unicode(vs_subnet),
        'vs_first_address': unicode(vs_first_address),
        'vs_v6_subnet': unicode(vs_v6_subnet),
        'vs_v6_first_address': unicode(vs_v6_first_address),
        'member_subnet': unicode(member_subnet),
        'member_first_address': unicode(member_first_address),
        'member_v6_subnet': unicode(member_v6_subnet),
        'member_v6_first_address': unicode(member_v6_first_address)
    }
    return config


def run_legacy_functional_tests(bip_client, config, delete_overrides):
    logger = logging.getLogger(__name__)

    for payload_file in get_payload_list(config):

        payload = load_payload(config['payloads_dir'], payload_file)
        payload_file_name = os.path.splitext(os.path.basename(payload_file))[0]

        test_run_log_dir = os.path.abspath(
            os.path.join("logs", config['session_id'],
                         'run', payload['name'])
        )

        for run in range(config['retries']):
            try:
                logger.info('{}/{} Deploying: {}'.format(
                    run, config['retries'], payload_file_name))

                app_deployed = bip_client.deploy_app_service(payload)

                logger.info('{}/{} Verifying deployment of: {}'.format(
                    run, config['retries'], payload_file_name))

                deployment_verified = bip_client.verify_deployment_result(
                    payload, test_run_log_dir)

                if payload_file_name in delete_overrides:
                    logger.info("Skipping removal of {},"
                                " due to 'test_delete_override'"
                                " flag set in payload template".format(
                                    payload_file_name))
                else:
                    logger.info("{}/{} Removing payload {}".format(
                        run, config['retries'], payload_file_name))
                    bip_client.remove_app_service(payload)

                if app_deployed and deployment_verified:
                    break

            except (AppServiceDeploymentException,
                    RESTException,
                    AppServiceDeploymentVerificationException,
                    AppServiceRemovalException) as ex:
                logger.exception(ex)
                if run+1 == config['retries']:
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


def get_payload_list(config):
    payloads = sorted(glob(os.path.join(config['payloads_dir'], "*.json")))
    return payloads[config['start']:config['end']]


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
