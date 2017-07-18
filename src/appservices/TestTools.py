#!/usr/bin/env python
import errno
import json
import os
import time
from glob import glob

import ipaddress

from src.appservices.PayloadGenerator import PayloadGenerator

from BIPClient import BIPClient


def prepare_payloads_functional_test(session_id, host, policy_host):

    payloads_dir = os.path.abspath(
        os.path.join("logs", session_id, 'payloads'))
    tmp_dir = os.path.abspath(
        os.path.join("logs", session_id, 'tmp')
    )
    flat_templates_dir = os.path.abspath(
        os.path.join("logs", session_id, 'payload_templates')
    )

    pay_gen = PayloadGenerator(
        os.getcwd(),
        payloads_dir,
        tmp_dir,
        flat_templates_dir
    )

    bip = BIPClient(host)
    version = bip.get_version()

    for payload_template in glob(os.path.join("payload_templates", "*.tmpl")):
        pay_gen.fill_template(
            payload_template, version, policy_host,
            u"172.16.0.0/24",
            u"2001:dead:beef:1::/120",
            u"172.16.0.100",
            u"2001:dead:beef:1::10",
            u"10.0.0.0/24",
            u"2001:dead:beef:2::/120",
            u"10.0.0.10",
            u"2001:dead:beef:2::10")

    for payload_template in glob(os.path.join(tmp_dir, "*.tmpl")):
        pay_gen.build_template(
            tmp_dir,
            payload_template,
            'admin',
            'admin'
        )

    app_service_template_name = bip.get_template_name()

    for payload_template in glob(os.path.join(flat_templates_dir, "*.tmpl")):
        pay_gen.build_bip_payload(payload_template, app_service_template_name)

