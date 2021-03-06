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

from src.appservices.TestTools import build_application_service_payloads
from src.appservices.TestTools import get_payload_files
from src.appservices.TestTools import get_test_config
from src.appservices.TestTools import strip_payload_name
from src.appservices.TestTools import update_payload_name
from src.appservices.TestTools import payload_is_build_in
from src.appservices.TestTools import get_payload_template_basename
from src.appservices.TestTools import get_payload_dependencies
from src.appservices.TestTools import check_delete_override
from src.appservices.TestTools import get_payload_basename


def test_dependant_payloads():
    config = get_test_config(
        "192.168.0.1", "192.168.0.2", timestamp='unit_test')

    dependants = build_application_service_payloads(config, {
        'version': "123",
        'major': "123",
        'minor': "123"
    })

    # I can not wait for the day
    #  when we remove this 'payload dependency mechanism'
    assert len(dependants.keys()) >= 8

    test_pools = get_payload_dependencies(dependants, 'test_pools')
    assert 5 == len(test_pools)

    assert test_pools[0]['name'] == 'test_pools'
    assert test_pools[0]['parent'] is True
    assert test_pools[0]['delete_override'] is True

    assert test_pools[2]['name'] == 'test_pools_3'
    assert test_pools[2]['parent'] is False
    assert test_pools[2]['delete_override'] is True

    assert test_pools[4]['name'] == 'test_pools_noindex'
    assert test_pools[4]['parent'] is False
    assert test_pools[4]['delete_override'] is False

    test_pools_3 = get_payload_dependencies(dependants, 'test_pools_3')

    assert 3 == len(test_pools_3)

    assert test_pools_3[0]['name'] == 'test_pools_3'
    assert test_pools_3[0]['delete_override'] is True

    for pool in test_pools_3:
        assert pool['parent'] is False

    test_pools_noindex = get_payload_dependencies(dependants, 'test_pools_noindex')

    assert 1 == len(test_pools_noindex)

    assert test_pools_noindex[0]['name'] == 'test_pools_noindex'
    assert test_pools_noindex[0]['parent'] is False
    assert test_pools_noindex[0]['delete_override'] is False

    test_vs_standard_https_bundle_all_preserve = get_payload_dependencies(dependants, 'test_vs_standard_https_bundle_all_preserve')

    assert 2 == len(test_vs_standard_https_bundle_all_preserve)

    assert test_vs_standard_https_bundle_all_preserve[0]['name'] == 'test_vs_standard_https_bundle_all_preserve'
    assert test_vs_standard_https_bundle_all_preserve[0]['parent'] is True
    assert test_vs_standard_https_bundle_all_preserve[0]['delete_override'] is True

    assert test_vs_standard_https_bundle_all_preserve[1]['name'] == 'test_vs_standard_https_bundle_all_preserve_2'
    assert test_vs_standard_https_bundle_all_preserve[1]['parent'] is False
    assert test_vs_standard_https_bundle_all_preserve[1]['delete_override'] is False

    assert get_payload_dependencies(dependants, 'test_vs_sctp') == []

    assert check_delete_override(
        get_payload_dependencies(dependants, 'test_vs_sctp'),
        'test_vs_sctp') is False

    assert check_delete_override(
        get_payload_dependencies(dependants, 'test_pools'),
        'test_pools_3') is True

    assert check_delete_override(
        get_payload_dependencies(dependants, 'test_pools'),
        'test_pools_4') is False


def test_get_payload_generation():
    config = get_test_config(
        "192.168.0.1", "192.168.0.2", start=0, end=5, timestamp='unit_test')
    build_application_service_payloads(config, {
        'version': "123",
        'major': "123",
        'minor': "123"
    })
    payloads = get_payload_files(config)

    assert len(payloads) == 5

    payload_base_name = get_payload_basename(payloads[0])

    assert payload_base_name == 'test_monitors'


def test_payload_template_basename():
    assert get_payload_template_basename('test_pools.template.json') == 'test_pools'


def test_build_in_payload():
    assert payload_is_build_in('test_pools.template.json')


def test_update_payload_name_and_strip_payload_name():
    payload_names = [
        'include_defaults',
        'test_monitors_noindex',
        'test_monitors',
        'test_pools_2',
        'test_pools_3',
        'test_pools_4',
        'test_pools_fixup_2',
        'test_pools_fixup_3',
        'test_pools_fixup_4',
        'test_pools_fixup',
        'test_pools_noindex',
        'test_pools',
        'test_vs_fasthttp_tcp',
        'test_vs_fastl4_tcp',
        'test_vs_fastl4_udp',
        'test_vs_ipforward_emptypool',
        'test_vs_ipforward',
        'test_vs_ipother',
        'test_vs_sctp',
        'test_vs_standard_http_afm',
        'test_vs_standard_http_autoxff',
        'test_vs_standard_http_bundle_irule',
        'test_vs_standard_http_ipv6',
        'test_vs_standard_http_options_2',
        'test_vs_standard_http_options',
        'test_vs_standard_https_bundle_all_preserve_2',
        'test_vs_standard_https_bundle_all_preserve',
        'test_vs_standard_https_bundle_all_redeploy_2',
        'test_vs_standard_https_bundle_all_redeploy',
        'test_vs_standard_https_bundle_all_url',
        'test_vs_standard_https_bundle_apm_preserve_2',
        'test_vs_standard_https_bundle_apm_preserve',
        'test_vs_standard_https_bundle_apm_redeploy_2',
        'test_vs_standard_https_bundle_apm_redeploy',
        'test_vs_standard_https_bundle_asm_preserve_2',
        'test_vs_standard_https_bundle_asm_preserve',
        'test_vs_standard_https_bundle_asm_redeploy_2',
        'test_vs_standard_https_bundle_asm_redeploy',
        'test_vs_standard_https_create',
        'test_vs_standard_https_create_url_partition',
        'test_vs_standard_https_create_url',
        'test_vs_standard_https_features',
        'test_vs_standard_https_l7policy',
        'test_vs_standard_https_multi_listeners',
        'test_vs_standard_https_serverssl_create',
        'test_vs_standard_https_serverssl',
        'test_vs_standard_https',
        'test_vs_standard_http',
        'test_vs_standard_tcp_afm',
        'test_vs_standard_tcp_options',
        'test_vs_standard_tcp_rd_auto',
        'test_vs_standard_tcp_rd_nonauto',
        'test_vs_standard_tcp_routeadv_all',
        'test_vs_standard_tcp_routeadv_always',
        'test_vs_standard_tcp_routeadv_any',
        'test_vs_standard_tcp',
        'test_vs_standard_tcp_virt_addr_options',
        'test_vs_standard_udp_afm',
        'test_vs_standard_udp',
        'test_without_vs_Name']

    for payload_name in payload_names:
        assert update_payload_name(payload_name, 7) == "{}__{}".format(
            strip_payload_name(payload_name), 7)

        assert update_payload_name(payload_name, 13) == "{}__{}".format(
            strip_payload_name(payload_name), 13)
