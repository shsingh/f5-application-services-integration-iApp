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
| test_monitors.ptmpl_                                   | - HTTP 200       | LTM Virtual Server, Monitor & Pool creation.  Monitor   |
|                                                       | - Deployment_    | types:                                                  |
|                                                       |                  |                                                         |
|                                                       |                  | - TCP default                                           |
|                                                       |                  | - HTTP default                                          |
|                                                       |                  | - HTTP custom inline (ASO encapsulated)                 |
|                                                       |                  | - HTTP pre-existing by ref                              |
+-------------------------------------------------------+------------------+-------------------+-------------------------------------+
| test_monitors_noindex.ptmpl_                           | - HTTP 200       | LTM Virtual Server, Monitor & Pool creation.  Monitor   |
|                                                       | - Deployment_    | purposely omits Index.  Monitor types:                  |
|                                                       |                  |                                                         |
|                                                       |                  | - TCP default                                           |
+-------------------------------------------------------+------------------+---------------------------------------------------------+
| test_pools.ptmpl_                                      | - HTTP 200       | LTM Virtual Server, Monitor, Pool & Pool Member         |
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
| test_pools_2.ptmpl_                                    | - HTTP 200       | coming soon                                             |
|                                                       | - Deployment_    |                                                         |
+-------------------------------------------------------+------------------+---------------------------------------------------------+
| test_pools_3.ptmpl_                                    | - HTTP 200       | coming soon                                             |
|                                                       | - Deployment_    |                                                         |
+-------------------------------------------------------+------------------+---------------------------------------------------------+
| test_pools_4.ptmpl_                                    | - HTTP 200       | coming soon                                             |
|                                                       | - Deployment_    |                                                         |
+-------------------------------------------------------+------------------+---------------------------------------------------------+
| test_pools_fixup.ptmpl_                                | - HTTP 200       | coming soon                                             |
|                                                       | - Deployment_    |                                                         |
+-------------------------------------------------------+------------------+---------------------------------------------------------+
| test_pools_fixup_2.ptmpl_                              | - HTTP 200       | coming soon                                             |
|                                                       | - Deployment_    |                                                         |
+-------------------------------------------------------+------------------+---------------------------------------------------------+
| test_pools_fixup_3.ptmpl_                              | - HTTP 200       | coming soon                                             |
|                                                       | - Deployment_    |                                                         |
+-------------------------------------------------------+------------------+---------------------------------------------------------+
| test_pools_fixup_4.ptmpl_                              | - HTTP 200       | coming soon                                             |
|                                                       | - Deployment_    |                                                         |
+-------------------------------------------------------+------------------+---------------------------------------------------------+
| test_pools_noindex.ptmpl_                              | - HTTP 200       | coming soon                                             |
|                                                       | - Deployment_    |                                                         |
+-------------------------------------------------------+------------------+---------------------------------------------------------+
| test_vs_fasthttp_tcp.ptmpl_                            | - HTTP 200       | coming soon                                             |
|                                                       | - Deployment_    |                                                         |
+-------------------------------------------------------+------------------+---------------------------------------------------------+
| test_vs_fastl4_tcp.ptmpl_                              | - HTTP 200       | coming soon                                             |
|                                                       | - Deployment_    |                                                         |
+-------------------------------------------------------+------------------+---------------------------------------------------------+
| test_vs_fastl4_udp.ptmpl_                              | - HTTP 200       | coming soon                                             |
|                                                       | - Deployment_    |                                                         |
+-------------------------------------------------------+------------------+---------------------------------------------------------+
| test_vs_ipforward.ptmpl_                               | - HTTP 200       | coming soon                                             |
|                                                       | - Deployment_    |                                                         |
+-------------------------------------------------------+------------------+---------------------------------------------------------+
| test_vs_ipforward_emptypool.ptmpl_                     | - HTTP 200       | coming soon                                             |
|                                                       | - Deployment_    |                                                         |
+-------------------------------------------------------+------------------+---------------------------------------------------------+
| test_vs_ipother.ptmpl_                                 | - HTTP 200       | coming soon                                             |
|                                                       | - Deployment_    |                                                         |
+-------------------------------------------------------+------------------+---------------------------------------------------------+
| test_vs_sctp.ptmpl_                                    | - HTTP 200       | coming soon                                             |
|                                                       | - Deployment_    |                                                         |
+-------------------------------------------------------+------------------+---------------------------------------------------------+
| test_vs_standard_http.ptmpl_                           | - HTTP 200       | coming soon                                             |
|                                                       | - Deployment_    |                                                         |
+-------------------------------------------------------+------------------+---------------------------------------------------------+
| test_vs_standard_http_afm.ptmpl_                       | - HTTP 200       | coming soon                                             |
|                                                       | - Deployment_    |                                                         |
+-------------------------------------------------------+------------------+---------------------------------------------------------+
| test_vs_standard_http_autoxff.ptmpl_                   | - HTTP 200       | coming soon                                             |
|                                                       | - Deployment_    |                                                         |
+-------------------------------------------------------+------------------+---------------------------------------------------------+
| test_vs_standard_http_bundle_irule.ptmpl_              | - HTTP 200       | coming soon                                             |
|                                                       | - Deployment_    |                                                         |
+-------------------------------------------------------+------------------+---------------------------------------------------------+
| test_vs_standard_http_ipv6.ptmpl_                      | - HTTP 200       | coming soon                                             |
|                                                       | - Deployment_    |                                                         |
+-------------------------------------------------------+------------------+---------------------------------------------------------+
| test_vs_standard_http_options.ptmpl_                   | - HTTP 200       | coming soon                                             |
|                                                       | - Deployment_    |                                                         |
+-------------------------------------------------------+------------------+---------------------------------------------------------+
| test_vs_standard_http_options_2.ptmpl_                 | - HTTP 200       | coming soon                                             |
|                                                       | - Deployment_    |                                                         |
+-------------------------------------------------------+------------------+---------------------------------------------------------+
| test_vs_standard_https.ptmpl_                          | - HTTP 200       | coming soon                                             |
|                                                       | - Deployment_    |                                                         |
+-------------------------------------------------------+------------------+---------------------------------------------------------+
| test_vs_standard_https_bundle_all_preserve.ptmpl_      | - HTTP 200       | coming soon                                             |
|                                                       | - Deployment_    |                                                         |
+-------------------------------------------------------+------------------+---------------------------------------------------------+
| test_vs_standard_https_bundle_all_preserve_2.ptmpl_    | - HTTP 200       | coming soon                                             |
|                                                       | - Deployment_    |                                                         |
+-------------------------------------------------------+------------------+---------------------------------------------------------+
| test_vs_standard_https_bundle_all_redeploy.ptmpl_      | - HTTP 200       | coming soon                                             |
|                                                       | - Deployment_    |                                                         |
+-------------------------------------------------------+------------------+---------------------------------------------------------+
| test_vs_standard_https_bundle_all_redeploy_2.ptmpl_    | - HTTP 200       | coming soon                                             |
|                                                       | - Deployment_    |                                                         |
+-------------------------------------------------------+------------------+---------------------------------------------------------+
| test_vs_standard_https_bundle_all_url.ptmpl_           | - HTTP 200       | coming soon                                             |
|                                                       | - Deployment_    |                                                         |
+-------------------------------------------------------+------------------+---------------------------------------------------------+
| test_vs_standard_https_bundle_apm_preserve.ptmpl_      | - HTTP 200       | coming soon                                             |
|                                                       | - Deployment_    |                                                         |
+-------------------------------------------------------+------------------+---------------------------------------------------------+
| test_vs_standard_https_bundle_apm_preserve_2.ptmpl_    | - HTTP 200       | coming soon                                             |
|                                                       | - Deployment_    |                                                         |
+-------------------------------------------------------+------------------+---------------------------------------------------------+
| test_vs_standard_https_bundle_apm_redeploy.ptmpl_      | - HTTP 200       | coming soon                                             |
|                                                       | - Deployment_    |                                                         |
+-------------------------------------------------------+------------------+---------------------------------------------------------+
| test_vs_standard_https_bundle_apm_redeploy_2.ptmpl_    | - HTTP 200       | coming soon                                             |
|                                                       | - Deployment_    |                                                         |
+-------------------------------------------------------+------------------+---------------------------------------------------------+
| test_vs_standard_https_bundle_asm_preserve.ptmpl_      | - HTTP 200       | coming soon                                             |
|                                                       | - Deployment_    |                                                         |
+-------------------------------------------------------+------------------+---------------------------------------------------------+
| test_vs_standard_https_bundle_asm_preserve_2.ptmpl_    | - HTTP 200       | coming soon                                             |
|                                                       | - Deployment_    |                                                         |
+-------------------------------------------------------+------------------+---------------------------------------------------------+
| test_vs_standard_https_bundle_asm_redeploy.ptmpl_      | - HTTP 200       | coming soon                                             |
|                                                       | - Deployment_    |                                                         |
+-------------------------------------------------------+------------------+---------------------------------------------------------+
| test_vs_standard_https_bundle_asm_redeploy_2.ptmpl_    | - HTTP 200       | coming soon                                             |
|                                                       | - Deployment_    |                                                         |
+-------------------------------------------------------+------------------+---------------------------------------------------------+
| test_vs_standard_https_create.ptmpl_                   | - HTTP 200       | coming soon                                             |
|                                                       | - Deployment_    |                                                         |
+-------------------------------------------------------+------------------+---------------------------------------------------------+
| test_vs_standard_https_create_url.ptmpl_               | - HTTP 200       | coming soon                                             |
|                                                       | - Deployment_    |                                                         |
+-------------------------------------------------------+------------------+---------------------------------------------------------+
| test_vs_standard_https_create_url_partition.ptmpl_     | - HTTP 200       | coming soon                                             |
|                                                       | - Deployment_    |                                                         |
+-------------------------------------------------------+------------------+---------------------------------------------------------+
| test_vs_standard_https_features.ptmpl_                 | - HTTP 200       | coming soon                                             |
|                                                       | - Deployment_    |                                                         |
+-------------------------------------------------------+------------------+---------------------------------------------------------+
| test_vs_standard_https_l7policy.ptmpl_                 | - HTTP 200       | coming soon                                             |
|                                                       | - Deployment_    |                                                         |
+-------------------------------------------------------+------------------+---------------------------------------------------------+
| test_vs_standard_https_multi_listeners.ptmpl_          | - HTTP 200       | coming soon                                             |
|                                                       | - Deployment_    |                                                         |
+-------------------------------------------------------+------------------+---------------------------------------------------------+
| test_vs_standard_https_serverssl.ptmpl_                | - HTTP 200       | coming soon                                             |
|                                                       | - Deployment_    |                                                         |
+-------------------------------------------------------+------------------+---------------------------------------------------------+
| test_vs_standard_https_serverssl_create.ptmpl_         | - HTTP 200       | coming soon                                             |
|                                                       | - Deployment_    |                                                         |
+-------------------------------------------------------+------------------+---------------------------------------------------------+
| test_vs_standard_tcp.ptmpl_                            | - HTTP 200       | coming soon                                             |
|                                                       | - Deployment_    |                                                         |
+-------------------------------------------------------+------------------+---------------------------------------------------------+
| test_vs_standard_tcp_afm.ptmpl_                        | - HTTP 200       | coming soon                                             |
|                                                       | - Deployment_    |                                                         |
+-------------------------------------------------------+------------------+---------------------------------------------------------+
| test_vs_standard_tcp_options.ptmpl_                    | - HTTP 200       | coming soon                                             |
|                                                       | - Deployment_    |                                                         |
+-------------------------------------------------------+------------------+---------------------------------------------------------+
| test_vs_standard_tcp_rd_auto.ptmpl_                    | - HTTP 200       | coming soon                                             |
|                                                       | - Deployment_    |                                                         |
+-------------------------------------------------------+------------------+---------------------------------------------------------+
| test_vs_standard_tcp_rd_nonauto.ptmpl_                 | - HTTP 200       | coming soon                                             |
|                                                       | - Deployment_    |                                                         |
+-------------------------------------------------------+------------------+---------------------------------------------------------+
| test_vs_standard_tcp_routeadv_all.ptmpl_               | - HTTP 200       | coming soon                                             |
|                                                       | - Deployment_    |                                                         |
+-------------------------------------------------------+------------------+---------------------------------------------------------+
| test_vs_standard_tcp_routeadv_always.ptmpl_            | - HTTP 200       | coming soon                                             |
|                                                       | - Deployment_    |                                                         |
+-------------------------------------------------------+------------------+---------------------------------------------------------+
| test_vs_standard_tcp_routeadv_any.ptmpl_               | - HTTP 200       | coming soon                                             |
|                                                       | - Deployment_    |                                                         |
+-------------------------------------------------------+------------------+---------------------------------------------------------+
| test_vs_standard_tcp_virt_addr_options.ptmpl_          | - HTTP 200       | coming soon                                             |
|                                                       | - Deployment_    |                                                         |
+-------------------------------------------------------+------------------+---------------------------------------------------------+
| test_vs_standard_udp.ptmpl_                            | - HTTP 200       | coming soon                                             |
|                                                       | - Deployment_    |                                                         |
+-------------------------------------------------------+------------------+---------------------------------------------------------+
| test_vs_standard_udp_afm.ptmpl_                        | - HTTP 200       | coming soon                                             |
|                                                       | - Deployment_    |                                                         |
+-------------------------------------------------------+------------------+---------------------------------------------------------+

.. _Deployment: https://devcentral.f5.com/wiki/iApp.AppSvcsiApp_execflow.ashx#determining-success-failure-of-deployment
.. _test_monitors.ptmpl: test_monitors.ptmpl
.. _test_monitors_noindex.ptmpl: test_monitors_noindex.ptmpl
.. _test_pools.ptmpl: test_pools.ptmpl
.. _test_pools_2.ptmpl: test_pools_2.ptmpl
.. _test_pools_3.ptmpl: test_pools_3.ptmpl
.. _test_pools_4.ptmpl: test_pools_4.ptmpl
.. _test_pools_fixup.ptmpl: test_pools_fixup.ptmpl
.. _test_pools_fixup_2.ptmpl: test_pools_fixup_2.ptmpl
.. _test_pools_fixup_3.ptmpl: test_pools_fixup_3.ptmpl
.. _test_pools_fixup_4.ptmpl: test_pools_fixup_4.ptmpl
.. _test_pools_noindex.ptmpl: test_pools_noindex.ptmpl
.. _test_vs_fasthttp_tcp.ptmpl: test_vs_fasthttp_tcp.ptmpl
.. _test_vs_fastl4_tcp.ptmpl: test_vs_fastl4_tcp.ptmpl
.. _test_vs_fastl4_udp.ptmpl: test_vs_fastl4_udp.ptmpl
.. _test_vs_ipforward.ptmpl: test_vs_ipforward.ptmpl
.. _test_vs_ipforward_emptypool.ptmpl: test_vs_ipforward_emptypool.ptmpl
.. _test_vs_ipother.ptmpl: test_vs_ipother.ptmpl
.. _test_vs_sctp.ptmpl: test_vs_sctp.ptmpl
.. _test_vs_standard_http.ptmpl: test_vs_standard_http.ptmpl
.. _test_vs_standard_http_afm.ptmpl: test_vs_standard_http_afm.ptmpl
.. _test_vs_standard_http_autoxff.ptmpl: test_vs_standard_http_autoxff.ptmpl
.. _test_vs_standard_http_bundle_irule.ptmpl: test_vs_standard_http_bundle_irule.ptmpl
.. _test_vs_standard_http_ipv6.ptmpl: test_vs_standard_http_ipv6.ptmpl
.. _test_vs_standard_http_options.ptmpl: test_vs_standard_http_options.ptmpl
.. _test_vs_standard_http_options_2.ptmpl: test_vs_standard_http_options_2.ptmpl
.. _test_vs_standard_https.ptmpl: test_vs_standard_https.ptmpl
.. _test_vs_standard_https_bundle_all_preserve.ptmpl: test_vs_standard_https_bundle_all_preserve.ptmpl
.. _test_vs_standard_https_bundle_all_preserve_2.ptmpl: test_vs_standard_https_bundle_all_preserve_2.ptmpl
.. _test_vs_standard_https_bundle_all_redeploy.ptmpl: test_vs_standard_https_bundle_all_redeploy.ptmpl
.. _test_vs_standard_https_bundle_all_redeploy_2.ptmpl: test_vs_standard_https_bundle_all_redeploy_2.ptmpl
.. _test_vs_standard_https_bundle_all_url.ptmpl: test_vs_standard_https_bundle_all_url.ptmpl
.. _test_vs_standard_https_bundle_apm_preserve.ptmpl: test_vs_standard_https_bundle_apm_preserve.ptmpl
.. _test_vs_standard_https_bundle_apm_preserve_2.ptmpl: test_vs_standard_https_bundle_apm_preserve_2.ptmpl
.. _test_vs_standard_https_bundle_apm_redeploy.ptmpl: test_vs_standard_https_bundle_apm_redeploy.ptmpl
.. _test_vs_standard_https_bundle_apm_redeploy_2.ptmpl: test_vs_standard_https_bundle_apm_redeploy_2.ptmpl
.. _test_vs_standard_https_bundle_asm_preserve.ptmpl: test_vs_standard_https_bundle_asm_preserve.ptmpl
.. _test_vs_standard_https_bundle_asm_preserve_2.ptmpl: test_vs_standard_https_bundle_asm_preserve_2.ptmpl
.. _test_vs_standard_https_bundle_asm_redeploy.ptmpl: test_vs_standard_https_bundle_asm_redeploy.ptmpl
.. _test_vs_standard_https_bundle_asm_redeploy_2.ptmpl: test_vs_standard_https_bundle_asm_redeploy_2.ptmpl
.. _test_vs_standard_https_create.ptmpl: test_vs_standard_https_create.ptmpl
.. _test_vs_standard_https_create_url.ptmpl: test_vs_standard_https_create_url.ptmpl
.. _test_vs_standard_https_create_url_partition.ptmpl: test_vs_standard_https_create_url_partition.ptmpl
.. _test_vs_standard_https_features.ptmpl: test_vs_standard_https_features.ptmpl
.. _test_vs_standard_https_l7policy.ptmpl: test_vs_standard_https_l7policy.ptmpl
.. _test_vs_standard_https_multi_listeners.ptmpl: test_vs_standard_https_multi_listeners.ptmpl
.. _test_vs_standard_https_serverssl.ptmpl: test_vs_standard_https_serverssl.ptmpl
.. _test_vs_standard_https_serverssl_create.ptmpl: test_vs_standard_https_serverssl_create.ptmpl
.. _test_vs_standard_tcp.ptmpl: test_vs_standard_tcp.ptmpl
.. _test_vs_standard_tcp_afm.ptmpl: test_vs_standard_tcp_afm.ptmpl
.. _test_vs_standard_tcp_options.ptmpl: test_vs_standard_tcp_options.ptmpl
.. _test_vs_standard_tcp_rd_auto.ptmpl: test_vs_standard_tcp_rd_auto.ptmpl
.. _test_vs_standard_tcp_rd_nonauto.ptmpl: test_vs_standard_tcp_rd_nonauto.ptmpl
.. _test_vs_standard_tcp_routeadv_all.ptmpl: test_vs_standard_tcp_routeadv_all.ptmpl
.. _test_vs_standard_tcp_routeadv_always.ptmpl: test_vs_standard_tcp_routeadv_always.ptmpl
.. _test_vs_standard_tcp_routeadv_any.ptmpl: test_vs_standard_tcp_routeadv_any.ptmpl
.. _test_vs_standard_tcp_virt_addr_options.ptmpl: test_vs_standard_tcp_virt_addr_options.ptmpl
.. _test_vs_standard_udp.ptmpl: test_vs_standard_udp.ptmpl
.. _test_vs_standard_udp_afm.ptmpl: test_vs_standard_udp_afm.ptmpl


iWorkflow

+---------------------------------------+----------------------------------+---------------------------------------------------------+
| Test Case                             | Success Criteria                 | Summary                                                 |
+=======================================+==================================+=========================================================+
| coming soon                           |                                  |                                                         |
+---------------------------------------+----------------------------------+---------------------------------------------------------+

Contributing
------------

See `Contributing <https://github.com/F5Networks/f5-application-services-integration-iApp/blob/release/v2.0.002/CONTRIBUTING.md>`_ for information on how to contribute and expectations around test coverage in contributions.
