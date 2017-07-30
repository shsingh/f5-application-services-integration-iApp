#!/usr/bin/env python

from src.appservices.TestTools import strip_payload_name
from src.appservices.TestTools import update_payload_name
from src.appservices.TestTools import get_payload_list
from src.appservices.TestTools import get_test_config
from src.appservices.TestTools import build_application_service_payloads
from src.appservices.TestTools import check_dependency


def test_get_payload_generation():
    config = get_test_config(
        "192.168.0.1", "192.168.0.2", start=0, end=5)
    dependants = build_application_service_payloads(config, {
        'version': "123",
        'major': "123",
        'minor': "123"
    })
    payloads = get_payload_list(config)

    assert len(payloads) == 5

    # I can not wait for the day
    #  when we remove this 'payload dependency mechanism'
    assert len(dependants.keys()) == 10

    #assert check_dependency('test_pools', dependants)


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
        'test_without_vs__Name']

    for payload_name in payload_names:
        assert update_payload_name(payload_name, 7) == "{}_{}".format(
            strip_payload_name(payload_name), 7)

        assert update_payload_name(payload_name, 13) == "{}_{}".format(
            strip_payload_name(payload_name), 13)
