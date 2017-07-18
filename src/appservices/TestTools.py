#!/usr/bin/env python
import logging
import os
from glob import glob

from BIPClient import BIPClient
from src.appservices.PayloadGenerator import PayloadGenerator


def prepare_payloads_functional_test(config):

    logging.basicConfig(level=logging.DEBUG)
    bip = BIPClient(
        config['host'],
        logging
    )

    bip.upload_files(
            ['upload_files/test_config.conf'],
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

