.. raw:: html

   <!--
   Copyright 2016-2017 F5 Networks Inc.

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
   -->

Application Services Integration iApp - Test Cases
=========================================================

Introduction
------------

Information on the individual test cases for BIG-IP and iWorkflow.

Documentation
-------------

Please refer to the F5 App Services Integration iApp `testing documentation <https://devcentral.f5.com/wiki/iApp.AppSvcsiApp_userguide_module4_lab3.ashx>`_ for more information on executing tests.

Test Cases
----------

BIG-IP

+-------------------------------------------------------+------------------+---------------------------------------------------------+
| Test Case                                             | Success Criteria | Scope  Summary                                          |
+=======================================================+==================+=========================================================+
| test_monitors.template.json_                          | - HTTP 200       | LTM Virtual Server, Monitor & Pool creation.  Monitor   |
|                                                       | - Deployment_    | types:                                                  |
|                                                       |                  |                                                         |
|                                                       |                  | - TCP default                                           |
|                                                       |                  | - HTTP default                                          |
|                                                       |                  | - HTTP custom inline (ASO encapsulated)                 |
|                                                       |                  | - HTTP pre-existing by ref                              |
+-------------------------------------------------------+------------------+-------------------+-------------------------------------+
| test_monitors_noindex.template.json_                  | - HTTP 200       | LTM Virtual Server, Monitor & Pool creation.  Monitor   |
|                                                       | - Deployment_    | purposely omits Index.  Monitor types:                  |
|                                                       |                  |                                                         |
|                                                       |                  | - TCP default                                           |
+-------------------------------------------------------+------------------+---------------------------------------------------------+
| test_pools.template.json_                             | - HTTP 200       | LTM Virtual Server, Monitor, Pool & Pool Member         |
|                                                       | - Deployment_    | creation.                                               |
|                                                       |                  |                                                         |
|                                                       |                  | Virtual Server:                                         |
|                                                       |                  |                                                         |
|                                                       |                  | - Address requested plus one?                           |
|                                                       |                  |                                                         |
|                                                       |                  | Monitor types:                                          |
|                                                       |                  |                                                         |
|                                                       |                  | - TCP default                                           |
|                                                       |                  | - HTTP default                                          |
|                                                       |                  |                                                         |
|                                                       |                  | Pools:                                                  |
|                                                       |                  |                                                         |
|                                                       |                  | - Default-named round robin w/ 3 members: 1 negative    |
|                                                       |                  |   and 1 duplicate                                       |
|                                                       |                  | - Explicit-named least connections w/ 13 members and    |
|                                                       |                  |   min of 2 active: 7 pre-existing by ref, 1 compound,   |
|                                                       |                  |   3 FQDN and 1 duplicate                                |
|                                                       |                  | - Explicit-named round robin w/ 2 members: many         |
|                                                       |                  |   duplicates and AdvOptions employed                    |
+-------------------------------------------------------+------------------+-------------------+-------------------------------------+
| test_pools_2.template.json_                           | - HTTP 200       | coming soon                                             |
|                                                       | - Deployment_    |                                                         |
+-------------------------------------------------------+------------------+---------------------------------------------------------+
| test_pools_3.template.json_                           | - HTTP 200       | coming soon                                             |
|                                                       | - Deployment_    |                                                         |
+-------------------------------------------------------+------------------+---------------------------------------------------------+
| test_pools_4.template.json_                           | - HTTP 200       | coming soon                                             |
|                                                       | - Deployment_    |                                                         |
+-------------------------------------------------------+------------------+---------------------------------------------------------+
| test_pools_fixup.template.json_                       | - HTTP 200       | coming soon                                             |
|                                                       | - Deployment_    |                                                         |
+-------------------------------------------------------+------------------+---------------------------------------------------------+
| test_pools_fixup_2.template.json_                     | - HTTP 200       | coming soon                                             |
|                                                       | - Deployment_    |                                                         |
+-------------------------------------------------------+------------------+---------------------------------------------------------+
| test_pools_fixup_3.template.json_                     | - HTTP 200       | coming soon                                             |
|                                                       | - Deployment_    |                                                         |
+-------------------------------------------------------+------------------+---------------------------------------------------------+
| test_pools_fixup_4.template.json_                     | - HTTP 200       | coming soon                                             |
|                                                       | - Deployment_    |                                                         |
+-------------------------------------------------------+------------------+---------------------------------------------------------+
| test_pools_noindex.template.json_                     | - HTTP 200       | coming soon                                             |
|                                                       | - Deployment_    |                                                         |
+-------------------------------------------------------+------------------+---------------------------------------------------------+
| test_vs_fasthttp_tcp.template.json_                   | - HTTP 200       | coming soon                                             |
|                                                       | - Deployment_    |                                                         |
+-------------------------------------------------------+------------------+---------------------------------------------------------+
| test_vs_fastl4_tcp.template.json_                     | - HTTP 200       | coming soon                                             |
|                                                       | - Deployment_    |                                                         |
+-------------------------------------------------------+------------------+---------------------------------------------------------+
| test_vs_fastl4_udp.template.json_                     | - HTTP 200       | coming soon                                             |
|                                                       | - Deployment_    |                                                         |
+-------------------------------------------------------+------------------+---------------------------------------------------------+
| test_vs_ipforward.template.json_                      | - HTTP 200       | coming soon                                             |
|                                                       | - Deployment_    |                                                         |
+-------------------------------------------------------+------------------+---------------------------------------------------------+
| test_vs_ipforward_emptypool.template.json_            | - HTTP 200       | coming soon                                             |
|                                                       | - Deployment_    |                                                         |
+-------------------------------------------------------+------------------+---------------------------------------------------------+
| test_vs_ipother.template.json_                        | - HTTP 200       | coming soon                                             |
|                                                       | - Deployment_    |                                                         |
+-------------------------------------------------------+------------------+---------------------------------------------------------+
| test_vs_sctp.template.json_                           | - HTTP 200       | coming soon                                             |
|                                                       | - Deployment_    |                                                         |
+-------------------------------------------------------+------------------+---------------------------------------------------------+
| test_vs_standard_http.template.json_                  | - HTTP 200       | coming soon                                             |
|                                                       | - Deployment_    |                                                         |
+-------------------------------------------------------+------------------+---------------------------------------------------------+
| test_vs_standard_http_afm.template.json_              | - HTTP 200       | coming soon                                             |
|                                                       | - Deployment_    |                                                         |
+-------------------------------------------------------+------------------+---------------------------------------------------------+
| test_vs_standard_http_autoxff.template.json_          | - HTTP 200       | coming soon                                             |
|                                                       | - Deployment_    |                                                         |
+-------------------------------------------------------+------------------+---------------------------------------------------------+
| test_vs_standard_http_bundle_irule.template.json_     | - HTTP 200       | coming soon                                             |
|                                                       | - Deployment_    |                                                         |
+-------------------------------------------------------+------------------+---------------------------------------------------------+
| test_vs_standard_http_ipv6.template.json_             | - HTTP 200       | coming soon                                             |
|                                                       | - Deployment_    |                                                         |
+-------------------------------------------------------+------------------+---------------------------------------------------------+
| test_vs_standard_http_options.template.json_          | - HTTP 200       | coming soon                                             |
|                                                       | - Deployment_    |                                                         |
+-------------------------------------------------------+------------------+---------------------------------------------------------+
| test_vs_standard_http_options_2.template.json_        | - HTTP 200       | coming soon                                             |
|                                                       | - Deployment_    |                                                         |
+-------------------------------------------------------+------------------+---------------------------------------------------------+
| test_vs_standard_https.template.json_                 | - HTTP 200       | coming soon                                             |
|                                                       | - Deployment_    |                                                         |
+-------------------------------------------------------+------------------+---------------------------------------------------------+
| test_vs_standard_https_bundle_all_preserve.template.json_      | - HTTP 200       | coming soon                                             |
|                                                       | - Deployment_    |                                                         |
+-------------------------------------------------------+------------------+---------------------------------------------------------+
| test_vs_standard_https_bundle_all_preserve_2.template.json_    | - HTTP 200       | coming soon                                             |
|                                                       | - Deployment_    |                                                         |
+-------------------------------------------------------+------------------+---------------------------------------------------------+
| test_vs_standard_https_bundle_all_redeploy.template.json_      | - HTTP 200       | coming soon                                             |
|                                                       | - Deployment_    |                                                         |
+-------------------------------------------------------+------------------+---------------------------------------------------------+
| test_vs_standard_https_bundle_all_redeploy_2.template.json_    | - HTTP 200       | coming soon                                             |
|                                                       | - Deployment_    |                                                         |
+-------------------------------------------------------+------------------+---------------------------------------------------------+
| test_vs_standard_https_bundle_all_url.template.json_           | - HTTP 200       | coming soon                                             |
|                                                       | - Deployment_    |                                                         |
+-------------------------------------------------------+------------------+---------------------------------------------------------+
| test_vs_standard_https_bundle_apm_preserve.template.json_      | - HTTP 200       | coming soon                                             |
|                                                       | - Deployment_    |                                                         |
+-------------------------------------------------------+------------------+---------------------------------------------------------+
| test_vs_standard_https_bundle_apm_preserve_2.template.json_    | - HTTP 200       | coming soon                                             |
|                                                       | - Deployment_    |                                                         |
+-------------------------------------------------------+------------------+---------------------------------------------------------+
| test_vs_standard_https_bundle_apm_redeploy.template.json_      | - HTTP 200       | coming soon                                             |
|                                                       | - Deployment_    |                                                         |
+-------------------------------------------------------+------------------+---------------------------------------------------------+
| test_vs_standard_https_bundle_apm_redeploy_2.template.json_    | - HTTP 200       | coming soon                                             |
|                                                       | - Deployment_    |                                                         |
+-------------------------------------------------------+------------------+---------------------------------------------------------+
| test_vs_standard_https_bundle_asm_preserve.template.json_      | - HTTP 200       | coming soon                                             |
|                                                       | - Deployment_    |                                                         |
+-------------------------------------------------------+------------------+---------------------------------------------------------+
| test_vs_standard_https_bundle_asm_preserve_2.template.json_    | - HTTP 200       | coming soon                                             |
|                                                       | - Deployment_    |                                                         |
+-------------------------------------------------------+------------------+---------------------------------------------------------+
| test_vs_standard_https_bundle_asm_redeploy.template.json_      | - HTTP 200       | coming soon                                             |
|                                                       | - Deployment_    |                                                         |
+-------------------------------------------------------+------------------+---------------------------------------------------------+
| test_vs_standard_https_bundle_asm_redeploy_2.template.json_    | - HTTP 200       | coming soon                                             |
|                                                       | - Deployment_    |                                                         |
+-------------------------------------------------------+------------------+---------------------------------------------------------+
| test_vs_standard_https_create.template.json_                   | - HTTP 200       | coming soon                                             |
|                                                       | - Deployment_    |                                                         |
+-------------------------------------------------------+------------------+---------------------------------------------------------+
| test_vs_standard_https_create_url.template.json_               | - HTTP 200       | coming soon                                             |
|                                                       | - Deployment_    |                                                         |
+-------------------------------------------------------+------------------+---------------------------------------------------------+
| test_vs_standard_https_create_url_partition.template.json_     | - HTTP 200       | coming soon                                             |
|                                                       | - Deployment_    |                                                         |
+-------------------------------------------------------+------------------+---------------------------------------------------------+
| test_vs_standard_https_features.template.json_                 | - HTTP 200       | coming soon                                             |
|                                                       | - Deployment_    |                                                         |
+-------------------------------------------------------+------------------+---------------------------------------------------------+
| test_vs_standard_https_l7policy.template.json_                 | - HTTP 200       | coming soon                                             |
|                                                       | - Deployment_    |                                                         |
+-------------------------------------------------------+------------------+---------------------------------------------------------+
| test_vs_standard_https_multi_listeners.template.json_          | - HTTP 200       | coming soon                                             |
|                                                       | - Deployment_    |                                                         |
+-------------------------------------------------------+------------------+---------------------------------------------------------+
| test_vs_standard_https_serverssl.template.json_                | - HTTP 200       | coming soon                                             |
|                                                       | - Deployment_    |                                                         |
+-------------------------------------------------------+------------------+---------------------------------------------------------+
| test_vs_standard_https_serverssl_create.template.json_         | - HTTP 200       | coming soon                                             |
|                                                       | - Deployment_    |                                                         |
+-------------------------------------------------------+------------------+---------------------------------------------------------+
| test_vs_standard_tcp.template.json_                            | - HTTP 200       | coming soon                                             |
|                                                       | - Deployment_    |                                                         |
+-------------------------------------------------------+------------------+---------------------------------------------------------+
| test_vs_standard_tcp_afm.template.json_                        | - HTTP 200       | coming soon                                             |
|                                                       | - Deployment_    |                                                         |
+-------------------------------------------------------+------------------+---------------------------------------------------------+
| test_vs_standard_tcp_options.template.json_                    | - HTTP 200       | coming soon                                             |
|                                                       | - Deployment_    |                                                         |
+-------------------------------------------------------+------------------+---------------------------------------------------------+
| test_vs_standard_tcp_rd_auto.template.json_                    | - HTTP 200       | coming soon                                             |
|                                                       | - Deployment_    |                                                         |
+-------------------------------------------------------+------------------+---------------------------------------------------------+
| test_vs_standard_tcp_rd_nonauto.template.json_                 | - HTTP 200       | coming soon                                             |
|                                                       | - Deployment_    |                                                         |
+-------------------------------------------------------+------------------+---------------------------------------------------------+
| test_vs_standard_tcp_routeadv_all.template.json_               | - HTTP 200       | coming soon                                             |
|                                                       | - Deployment_    |                                                         |
+-------------------------------------------------------+------------------+---------------------------------------------------------+
| test_vs_standard_tcp_routeadv_always.template.json_            | - HTTP 200       | coming soon                                             |
|                                                       | - Deployment_    |                                                         |
+-------------------------------------------------------+------------------+---------------------------------------------------------+
| test_vs_standard_tcp_routeadv_any.template.json_               | - HTTP 200       | coming soon                                             |
|                                                       | - Deployment_    |                                                         |
+-------------------------------------------------------+------------------+---------------------------------------------------------+
| test_vs_standard_tcp_virt_addr_options.template.json_          | - HTTP 200       | coming soon                                             |
|                                                       | - Deployment_    |                                                         |
+-------------------------------------------------------+------------------+---------------------------------------------------------+
| test_vs_standard_udp.template.json_                            | - HTTP 200       | coming soon                                             |
|                                                       | - Deployment_    |                                                         |
+-------------------------------------------------------+------------------+---------------------------------------------------------+
| test_vs_standard_udp_afm.template.json_                        | - HTTP 200       | coming soon                                             |
|                                                       | - Deployment_    |                                                         |
+-------------------------------------------------------+------------------+---------------------------------------------------------+

.. _Deployment: https://devcentral.f5.com/wiki/iApp.AppSvcsiApp_execflow.ashx#determining-success-failure-of-deployment
.. _test_monitors.template.json: test_monitors.template.json
.. _test_monitors_noindex.template.json: test_monitors_noindex.template.json
.. _test_pools.template.json: test_pools.template.json
.. _test_pools_2.template.json: test_pools_2.template.json
.. _test_pools_3.template.json: test_pools_3.template.json
.. _test_pools_4.template.json: test_pools_4.template.json
.. _test_pools_fixup.template.json: test_pools_fixup.template.json
.. _test_pools_fixup_2.template.json: test_pools_fixup_2.template.json
.. _test_pools_fixup_3.template.json: test_pools_fixup_3.template.json
.. _test_pools_fixup_4.template.json: test_pools_fixup_4.template.json
.. _test_pools_noindex.template.json: test_pools_noindex.template.json
.. _test_vs_fasthttp_tcp.template.json: test_vs_fasthttp_tcp.template.json
.. _test_vs_fastl4_tcp.template.json: test_vs_fastl4_tcp.template.json
.. _test_vs_fastl4_udp.template.json: test_vs_fastl4_udp.template.json
.. _test_vs_ipforward.template.json: test_vs_ipforward.template.json
.. _test_vs_ipforward_emptypool.template.json: test_vs_ipforward_emptypool.template.json
.. _test_vs_ipother.template.json: test_vs_ipother.template.json
.. _test_vs_sctp.template.json: test_vs_sctp.template.json
.. _test_vs_standard_http.template.json: test_vs_standard_http.template.json
.. _test_vs_standard_http_afm.template.json: test_vs_standard_http_afm.template.json
.. _test_vs_standard_http_autoxff.template.json: test_vs_standard_http_autoxff.template.json
.. _test_vs_standard_http_bundle_irule.template.json: test_vs_standard_http_bundle_irule.template.json
.. _test_vs_standard_http_ipv6.template.json: test_vs_standard_http_ipv6.template.json
.. _test_vs_standard_http_options.template.json: test_vs_standard_http_options.template.json
.. _test_vs_standard_http_options_2.template.json: test_vs_standard_http_options_2.template.json
.. _test_vs_standard_https.template.json: test_vs_standard_https.template.json
.. _test_vs_standard_https_bundle_all_preserve.template.json: test_vs_standard_https_bundle_all_preserve.template.json
.. _test_vs_standard_https_bundle_all_preserve_2.template.json: test_vs_standard_https_bundle_all_preserve_2.template.json
.. _test_vs_standard_https_bundle_all_redeploy.template.json: test_vs_standard_https_bundle_all_redeploy.template.json
.. _test_vs_standard_https_bundle_all_redeploy_2.template.json: test_vs_standard_https_bundle_all_redeploy_2.template.json
.. _test_vs_standard_https_bundle_all_url.template.json: test_vs_standard_https_bundle_all_url.template.json
.. _test_vs_standard_https_bundle_apm_preserve.template.json: test_vs_standard_https_bundle_apm_preserve.template.json
.. _test_vs_standard_https_bundle_apm_preserve_2.template.json: test_vs_standard_https_bundle_apm_preserve_2.template.json
.. _test_vs_standard_https_bundle_apm_redeploy.template.json: test_vs_standard_https_bundle_apm_redeploy.template.json
.. _test_vs_standard_https_bundle_apm_redeploy_2.template.json: test_vs_standard_https_bundle_apm_redeploy_2.template.json
.. _test_vs_standard_https_bundle_asm_preserve.template.json: test_vs_standard_https_bundle_asm_preserve.template.json
.. _test_vs_standard_https_bundle_asm_preserve_2.template.json: test_vs_standard_https_bundle_asm_preserve_2.template.json
.. _test_vs_standard_https_bundle_asm_redeploy.template.json: test_vs_standard_https_bundle_asm_redeploy.template.json
.. _test_vs_standard_https_bundle_asm_redeploy_2.template.json: test_vs_standard_https_bundle_asm_redeploy_2.template.json
.. _test_vs_standard_https_create.template.json: test_vs_standard_https_create.template.json
.. _test_vs_standard_https_create_url.template.json: test_vs_standard_https_create_url.template.json
.. _test_vs_standard_https_create_url_partition.template.json: test_vs_standard_https_create_url_partition.template.json
.. _test_vs_standard_https_features.template.json: test_vs_standard_https_features.template.json
.. _test_vs_standard_https_l7policy.template.json: test_vs_standard_https_l7policy.template.json
.. _test_vs_standard_https_multi_listeners.template.json: test_vs_standard_https_multi_listeners.template.json
.. _test_vs_standard_https_serverssl.template.json: test_vs_standard_https_serverssl.template.json
.. _test_vs_standard_https_serverssl_create.template.json: test_vs_standard_https_serverssl_create.template.json
.. _test_vs_standard_tcp.template.json: test_vs_standard_tcp.template.json
.. _test_vs_standard_tcp_afm.template.json: test_vs_standard_tcp_afm.template.json
.. _test_vs_standard_tcp_options.template.json: test_vs_standard_tcp_options.template.json
.. _test_vs_standard_tcp_rd_auto.template.json: test_vs_standard_tcp_rd_auto.template.json
.. _test_vs_standard_tcp_rd_nonauto.template.json: test_vs_standard_tcp_rd_nonauto.template.json
.. _test_vs_standard_tcp_routeadv_all.template.json: test_vs_standard_tcp_routeadv_all.template.json
.. _test_vs_standard_tcp_routeadv_always.template.json: test_vs_standard_tcp_routeadv_always.template.json
.. _test_vs_standard_tcp_routeadv_any.template.json: test_vs_standard_tcp_routeadv_any.template.json
.. _test_vs_standard_tcp_virt_addr_options.template.json: test_vs_standard_tcp_virt_addr_options.template.json
.. _test_vs_standard_udp.template.json: test_vs_standard_udp.template.json
.. _test_vs_standard_udp_afm.template.json: test_vs_standard_udp_afm.template.json


iWorkflow

+---------------------------------------+----------------------------------+---------------------------------------------------------+
| Test Case                             | Success Criteria                 | Summary                                                 |
+=======================================+==================================+=========================================================+
| coming soon                           |                                  |                                                         |
+---------------------------------------+----------------------------------+---------------------------------------------------------+

Contributing
------------

See `Contributing <https://github.com/F5Networks/f5-application-services-integration-iApp/blob/release/v2.0.002/CONTRIBUTING.md>`_ for information on how to contribute and expectations around test coverage in contributions.
