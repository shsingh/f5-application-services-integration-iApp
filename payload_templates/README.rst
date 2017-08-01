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
| test_monitors.tmpl_                                   | - HTTP 200       | LTM Virtual Server, Monitor & Pool creation.  Monitor   |
|                                                       | - Deployment_    | types:                                                  |
|                                                       |                  |                                                         |
|                                                       |                  | - TCP default                                           |
|                                                       |                  | - HTTP default                                          |
|                                                       |                  | - HTTP custom inline (ASO encapsulated)                 |
|                                                       |                  | - HTTP pre-existing by ref                              |
+-------------------------------------------------------+------------------+-------------------+-------------------------------------+
| test_monitors_noindex.tmpl_                           | - HTTP 200       | LTM Virtual Server, Monitor & Pool creation.  Monitor   |
|                                                       | - Deployment_    | purposely omits Index.  Monitor types:                  |
|                                                       |                  |                                                         |
|                                                       |                  | - TCP default                                           |
+-------------------------------------------------------+------------------+---------------------------------------------------------+
| test_pools.tmpl_                                      | - HTTP 200       | LTM Virtual Server, Monitor, Pool & Pool Member         |
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
| test_pools_2.tmpl_                                    | - HTTP 200       | coming soon                                             |
|                                                       | - Deployment_    |                                                         |
+-------------------------------------------------------+------------------+---------------------------------------------------------+
| test_pools_3.tmpl_                                    | - HTTP 200       | coming soon                                             |
|                                                       | - Deployment_    |                                                         |
+-------------------------------------------------------+------------------+---------------------------------------------------------+
| test_pools_4.tmpl_                                    | - HTTP 200       | coming soon                                             |
|                                                       | - Deployment_    |                                                         |
+-------------------------------------------------------+------------------+---------------------------------------------------------+
| test_pools_fixup.tmpl_                                | - HTTP 200       | coming soon                                             |
|                                                       | - Deployment_    |                                                         |
+-------------------------------------------------------+------------------+---------------------------------------------------------+
| test_pools_fixup_2.tmpl_                              | - HTTP 200       | coming soon                                             |
|                                                       | - Deployment_    |                                                         |
+-------------------------------------------------------+------------------+---------------------------------------------------------+
| test_pools_fixup_3.tmpl_                              | - HTTP 200       | coming soon                                             |
|                                                       | - Deployment_    |                                                         |
+-------------------------------------------------------+------------------+---------------------------------------------------------+
| test_pools_fixup_4.tmpl_                              | - HTTP 200       | coming soon                                             |
|                                                       | - Deployment_    |                                                         |
+-------------------------------------------------------+------------------+---------------------------------------------------------+
| test_pools_noindex.tmpl_                              | - HTTP 200       | coming soon                                             |
|                                                       | - Deployment_    |                                                         |
+-------------------------------------------------------+------------------+---------------------------------------------------------+
| test_vs_fasthttp_tcp.tmpl_                            | - HTTP 200       | coming soon                                             |
|                                                       | - Deployment_    |                                                         |
+-------------------------------------------------------+------------------+---------------------------------------------------------+
| test_vs_fastl4_tcp.tmpl_                              | - HTTP 200       | coming soon                                             |
|                                                       | - Deployment_    |                                                         |
+-------------------------------------------------------+------------------+---------------------------------------------------------+
| test_vs_fastl4_udp.tmpl_                              | - HTTP 200       | coming soon                                             |
|                                                       | - Deployment_    |                                                         |
+-------------------------------------------------------+------------------+---------------------------------------------------------+
| test_vs_ipforward.tmpl_                               | - HTTP 200       | coming soon                                             |
|                                                       | - Deployment_    |                                                         |
+-------------------------------------------------------+------------------+---------------------------------------------------------+
| test_vs_ipforward_emptypool.tmpl_                     | - HTTP 200       | coming soon                                             |
|                                                       | - Deployment_    |                                                         |
+-------------------------------------------------------+------------------+---------------------------------------------------------+
| test_vs_ipother.tmpl_                                 | - HTTP 200       | coming soon                                             |
|                                                       | - Deployment_    |                                                         |
+-------------------------------------------------------+------------------+---------------------------------------------------------+
| test_vs_sctp.tmpl_                                    | - HTTP 200       | coming soon                                             |
|                                                       | - Deployment_    |                                                         |
+-------------------------------------------------------+------------------+---------------------------------------------------------+
| test_vs_standard_http.tmpl_                           | - HTTP 200       | coming soon                                             |
|                                                       | - Deployment_    |                                                         |
+-------------------------------------------------------+------------------+---------------------------------------------------------+
| test_vs_standard_http_afm.tmpl_                       | - HTTP 200       | coming soon                                             |
|                                                       | - Deployment_    |                                                         |
+-------------------------------------------------------+------------------+---------------------------------------------------------+
| test_vs_standard_http_autoxff.tmpl_                   | - HTTP 200       | coming soon                                             |
|                                                       | - Deployment_    |                                                         |
+-------------------------------------------------------+------------------+---------------------------------------------------------+
| test_vs_standard_http_bundle_irule.tmpl_              | - HTTP 200       | coming soon                                             |
|                                                       | - Deployment_    |                                                         |
+-------------------------------------------------------+------------------+---------------------------------------------------------+
| test_vs_standard_http_ipv6.tmpl_                      | - HTTP 200       | coming soon                                             |
|                                                       | - Deployment_    |                                                         |
+-------------------------------------------------------+------------------+---------------------------------------------------------+
| test_vs_standard_http_options.tmpl_                   | - HTTP 200       | coming soon                                             |
|                                                       | - Deployment_    |                                                         |
+-------------------------------------------------------+------------------+---------------------------------------------------------+
| test_vs_standard_http_options_2.tmpl_                 | - HTTP 200       | coming soon                                             |
|                                                       | - Deployment_    |                                                         |
+-------------------------------------------------------+------------------+---------------------------------------------------------+
| test_vs_standard_https.tmpl_                          | - HTTP 200       | coming soon                                             |
|                                                       | - Deployment_    |                                                         |
+-------------------------------------------------------+------------------+---------------------------------------------------------+
| test_vs_standard_https_bundle_all_preserve.tmpl_      | - HTTP 200       | coming soon                                             |
|                                                       | - Deployment_    |                                                         |
+-------------------------------------------------------+------------------+---------------------------------------------------------+
| test_vs_standard_https_bundle_all_preserve_2.tmpl_    | - HTTP 200       | coming soon                                             |
|                                                       | - Deployment_    |                                                         |
+-------------------------------------------------------+------------------+---------------------------------------------------------+
| test_vs_standard_https_bundle_all_redeploy.tmpl_      | - HTTP 200       | coming soon                                             |
|                                                       | - Deployment_    |                                                         |
+-------------------------------------------------------+------------------+---------------------------------------------------------+
| test_vs_standard_https_bundle_all_redeploy_2.tmpl_    | - HTTP 200       | coming soon                                             |
|                                                       | - Deployment_    |                                                         |
+-------------------------------------------------------+------------------+---------------------------------------------------------+
| test_vs_standard_https_bundle_all_url.tmpl_           | - HTTP 200       | coming soon                                             |
|                                                       | - Deployment_    |                                                         |
+-------------------------------------------------------+------------------+---------------------------------------------------------+
| test_vs_standard_https_bundle_apm_preserve.tmpl_      | - HTTP 200       | coming soon                                             |
|                                                       | - Deployment_    |                                                         |
+-------------------------------------------------------+------------------+---------------------------------------------------------+
| test_vs_standard_https_bundle_apm_preserve_2.tmpl_    | - HTTP 200       | coming soon                                             |
|                                                       | - Deployment_    |                                                         |
+-------------------------------------------------------+------------------+---------------------------------------------------------+
| test_vs_standard_https_bundle_apm_redeploy.tmpl_      | - HTTP 200       | coming soon                                             |
|                                                       | - Deployment_    |                                                         |
+-------------------------------------------------------+------------------+---------------------------------------------------------+
| test_vs_standard_https_bundle_apm_redeploy_2.tmpl_    | - HTTP 200       | coming soon                                             |
|                                                       | - Deployment_    |                                                         |
+-------------------------------------------------------+------------------+---------------------------------------------------------+
| test_vs_standard_https_bundle_asm_preserve.tmpl_      | - HTTP 200       | coming soon                                             |
|                                                       | - Deployment_    |                                                         |
+-------------------------------------------------------+------------------+---------------------------------------------------------+
| test_vs_standard_https_bundle_asm_preserve_2.tmpl_    | - HTTP 200       | coming soon                                             |
|                                                       | - Deployment_    |                                                         |
+-------------------------------------------------------+------------------+---------------------------------------------------------+
| test_vs_standard_https_bundle_asm_redeploy.tmpl_      | - HTTP 200       | coming soon                                             |
|                                                       | - Deployment_    |                                                         |
+-------------------------------------------------------+------------------+---------------------------------------------------------+
| test_vs_standard_https_bundle_asm_redeploy_2.tmpl_    | - HTTP 200       | coming soon                                             |
|                                                       | - Deployment_    |                                                         |
+-------------------------------------------------------+------------------+---------------------------------------------------------+
| test_vs_standard_https_create.tmpl_                   | - HTTP 200       | coming soon                                             |
|                                                       | - Deployment_    |                                                         |
+-------------------------------------------------------+------------------+---------------------------------------------------------+
| test_vs_standard_https_create_url.tmpl_               | - HTTP 200       | coming soon                                             |
|                                                       | - Deployment_    |                                                         |
+-------------------------------------------------------+------------------+---------------------------------------------------------+
| test_vs_standard_https_create_url_partition.tmpl_     | - HTTP 200       | coming soon                                             |
|                                                       | - Deployment_    |                                                         |
+-------------------------------------------------------+------------------+---------------------------------------------------------+
| test_vs_standard_https_features.tmpl_                 | - HTTP 200       | coming soon                                             |
|                                                       | - Deployment_    |                                                         |
+-------------------------------------------------------+------------------+---------------------------------------------------------+
| test_vs_standard_https_l7policy.tmpl_                 | - HTTP 200       | coming soon                                             |
|                                                       | - Deployment_    |                                                         |
+-------------------------------------------------------+------------------+---------------------------------------------------------+
| test_vs_standard_https_multi_listeners.tmpl_          | - HTTP 200       | coming soon                                             |
|                                                       | - Deployment_    |                                                         |
+-------------------------------------------------------+------------------+---------------------------------------------------------+
| test_vs_standard_https_serverssl.tmpl_                | - HTTP 200       | coming soon                                             |
|                                                       | - Deployment_    |                                                         |
+-------------------------------------------------------+------------------+---------------------------------------------------------+
| test_vs_standard_https_serverssl_create.tmpl_         | - HTTP 200       | coming soon                                             |
|                                                       | - Deployment_    |                                                         |
+-------------------------------------------------------+------------------+---------------------------------------------------------+
| test_vs_standard_tcp.tmpl_                            | - HTTP 200       | coming soon                                             |
|                                                       | - Deployment_    |                                                         |
+-------------------------------------------------------+------------------+---------------------------------------------------------+
| test_vs_standard_tcp_afm.tmpl_                        | - HTTP 200       | coming soon                                             |
|                                                       | - Deployment_    |                                                         |
+-------------------------------------------------------+------------------+---------------------------------------------------------+
| test_vs_standard_tcp_options.tmpl_                    | - HTTP 200       | coming soon                                             |
|                                                       | - Deployment_    |                                                         |
+-------------------------------------------------------+------------------+---------------------------------------------------------+
| test_vs_standard_tcp_rd_auto.tmpl_                    | - HTTP 200       | coming soon                                             |
|                                                       | - Deployment_    |                                                         |
+-------------------------------------------------------+------------------+---------------------------------------------------------+
| test_vs_standard_tcp_rd_nonauto.tmpl_                 | - HTTP 200       | coming soon                                             |
|                                                       | - Deployment_    |                                                         |
+-------------------------------------------------------+------------------+---------------------------------------------------------+
| test_vs_standard_tcp_routeadv_all.tmpl_               | - HTTP 200       | coming soon                                             |
|                                                       | - Deployment_    |                                                         |
+-------------------------------------------------------+------------------+---------------------------------------------------------+
| test_vs_standard_tcp_routeadv_always.tmpl_            | - HTTP 200       | coming soon                                             |
|                                                       | - Deployment_    |                                                         |
+-------------------------------------------------------+------------------+---------------------------------------------------------+
| test_vs_standard_tcp_routeadv_any.tmpl_               | - HTTP 200       | coming soon                                             |
|                                                       | - Deployment_    |                                                         |
+-------------------------------------------------------+------------------+---------------------------------------------------------+
| test_vs_standard_tcp_virt_addr_options.tmpl_          | - HTTP 200       | coming soon                                             |
|                                                       | - Deployment_    |                                                         |
+-------------------------------------------------------+------------------+---------------------------------------------------------+
| test_vs_standard_udp.tmpl_                            | - HTTP 200       | coming soon                                             |
|                                                       | - Deployment_    |                                                         |
+-------------------------------------------------------+------------------+---------------------------------------------------------+
| test_vs_standard_udp_afm.tmpl_                        | - HTTP 200       | coming soon                                             |
|                                                       | - Deployment_    |                                                         |
+-------------------------------------------------------+------------------+---------------------------------------------------------+

.. _Deployment: https://devcentral.f5.com/wiki/iApp.AppSvcsiApp_execflow.ashx#determining-success-failure-of-deployment
.. _test_monitors.tmpl: test_monitors.tmpl
.. _test_monitors_noindex.tmpl: test_monitors_noindex.tmpl
.. _test_pools.tmpl: test_pools.tmpl
.. _test_pools_2.tmpl: test_pools_2.tmpl
.. _test_pools_3.tmpl: test_pools_3.tmpl
.. _test_pools_4.tmpl: test_pools_4.tmpl
.. _test_pools_fixup.tmpl: test_pools_fixup.tmpl
.. _test_pools_fixup_2.tmpl: test_pools_fixup_2.tmpl
.. _test_pools_fixup_3.tmpl: test_pools_fixup_3.tmpl
.. _test_pools_fixup_4.tmpl: test_pools_fixup_4.tmpl
.. _test_pools_noindex.tmpl: test_pools_noindex.tmpl
.. _test_vs_fasthttp_tcp.tmpl: test_vs_fasthttp_tcp.tmpl
.. _test_vs_fastl4_tcp.tmpl: test_vs_fastl4_tcp.tmpl
.. _test_vs_fastl4_udp.tmpl: test_vs_fastl4_udp.tmpl
.. _test_vs_ipforward.tmpl: test_vs_ipforward.tmpl
.. _test_vs_ipforward_emptypool.tmpl: test_vs_ipforward_emptypool.tmpl
.. _test_vs_ipother.tmpl: test_vs_ipother.tmpl
.. _test_vs_sctp.tmpl: test_vs_sctp.tmpl
.. _test_vs_standard_http.tmpl: test_vs_standard_http.tmpl
.. _test_vs_standard_http_afm.tmpl: test_vs_standard_http_afm.tmpl
.. _test_vs_standard_http_autoxff.tmpl: test_vs_standard_http_autoxff.tmpl
.. _test_vs_standard_http_bundle_irule.tmpl: test_vs_standard_http_bundle_irule.tmpl
.. _test_vs_standard_http_ipv6.tmpl: test_vs_standard_http_ipv6.tmpl
.. _test_vs_standard_http_options.tmpl: test_vs_standard_http_options.tmpl
.. _test_vs_standard_http_options_2.tmpl: test_vs_standard_http_options_2.tmpl
.. _test_vs_standard_https.tmpl: test_vs_standard_https.tmpl
.. _test_vs_standard_https_bundle_all_preserve.tmpl: test_vs_standard_https_bundle_all_preserve.tmpl
.. _test_vs_standard_https_bundle_all_preserve_2.tmpl: test_vs_standard_https_bundle_all_preserve_2.tmpl
.. _test_vs_standard_https_bundle_all_redeploy.tmpl: test_vs_standard_https_bundle_all_redeploy.tmpl
.. _test_vs_standard_https_bundle_all_redeploy_2.tmpl: test_vs_standard_https_bundle_all_redeploy_2.tmpl
.. _test_vs_standard_https_bundle_all_url.tmpl: test_vs_standard_https_bundle_all_url.tmpl
.. _test_vs_standard_https_bundle_apm_preserve.tmpl: test_vs_standard_https_bundle_apm_preserve.tmpl
.. _test_vs_standard_https_bundle_apm_preserve_2.tmpl: test_vs_standard_https_bundle_apm_preserve_2.tmpl
.. _test_vs_standard_https_bundle_apm_redeploy.tmpl: test_vs_standard_https_bundle_apm_redeploy.tmpl
.. _test_vs_standard_https_bundle_apm_redeploy_2.tmpl: test_vs_standard_https_bundle_apm_redeploy_2.tmpl
.. _test_vs_standard_https_bundle_asm_preserve.tmpl: test_vs_standard_https_bundle_asm_preserve.tmpl
.. _test_vs_standard_https_bundle_asm_preserve_2.tmpl: test_vs_standard_https_bundle_asm_preserve_2.tmpl
.. _test_vs_standard_https_bundle_asm_redeploy.tmpl: test_vs_standard_https_bundle_asm_redeploy.tmpl
.. _test_vs_standard_https_bundle_asm_redeploy_2.tmpl: test_vs_standard_https_bundle_asm_redeploy_2.tmpl
.. _test_vs_standard_https_create.tmpl: test_vs_standard_https_create.tmpl
.. _test_vs_standard_https_create_url.tmpl: test_vs_standard_https_create_url.tmpl
.. _test_vs_standard_https_create_url_partition.tmpl: test_vs_standard_https_create_url_partition.tmpl
.. _test_vs_standard_https_features.tmpl: test_vs_standard_https_features.tmpl
.. _test_vs_standard_https_l7policy.tmpl: test_vs_standard_https_l7policy.tmpl
.. _test_vs_standard_https_multi_listeners.tmpl: test_vs_standard_https_multi_listeners.tmpl
.. _test_vs_standard_https_serverssl.tmpl: test_vs_standard_https_serverssl.tmpl
.. _test_vs_standard_https_serverssl_create.tmpl: test_vs_standard_https_serverssl_create.tmpl
.. _test_vs_standard_tcp.tmpl: test_vs_standard_tcp.tmpl
.. _test_vs_standard_tcp_afm.tmpl: test_vs_standard_tcp_afm.tmpl
.. _test_vs_standard_tcp_options.tmpl: test_vs_standard_tcp_options.tmpl
.. _test_vs_standard_tcp_rd_auto.tmpl: test_vs_standard_tcp_rd_auto.tmpl
.. _test_vs_standard_tcp_rd_nonauto.tmpl: test_vs_standard_tcp_rd_nonauto.tmpl
.. _test_vs_standard_tcp_routeadv_all.tmpl: test_vs_standard_tcp_routeadv_all.tmpl
.. _test_vs_standard_tcp_routeadv_always.tmpl: test_vs_standard_tcp_routeadv_always.tmpl
.. _test_vs_standard_tcp_routeadv_any.tmpl: test_vs_standard_tcp_routeadv_any.tmpl
.. _test_vs_standard_tcp_virt_addr_options.tmpl: test_vs_standard_tcp_virt_addr_options.tmpl
.. _test_vs_standard_udp.tmpl: test_vs_standard_udp.tmpl
.. _test_vs_standard_udp_afm.tmpl: test_vs_standard_udp_afm.tmpl


iWorkflow

+---------------------------------------+----------------------------------+---------------------------------------------------------+
| Test Case                             | Success Criteria                 | Summary                                                 |
+=======================================+==================================+=========================================================+
| coming soon                           |                                  |                                                         |
+---------------------------------------+----------------------------------+---------------------------------------------------------+

Contributing
------------

See `Contributing <https://github.com/F5Networks/f5-application-services-integration-iApp/blob/release/v2.0.002/CONTRIBUTING.md>`_ for information on how to contribute and expectations around test coverage in contributions.
