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

+---------------------------------------+----------------------------------+---------------------------------------------------------+
| Test Case                             | Success Criteria                 | Scope  Summary                                          |
+=======================================+==================================+=========================================================+
| test_monitors.json_                   | - HTTP 200                       | LTM Virtual Server, Monitor & Pool creation.  Monitor   |
|                                       | - Deployment_                    | types:                                                  |
|                                       |                                  |                                                         |
|                                       |                                  | - TCP default                                           |
|                                       |                                  | - HTTP default                                          |
|                                       |                                  | - HTTP custom inline (ASO encapsulated)                 |
|                                       |                                  | - HTTP pre-existing by ref                              |
+---------------------------------------+----------------------------------+-------------------+-------------------------------------+
| test_monitors_noindex.json_           | - HTTP 200                       | LTM Virtual Server, Monitor & Pool creation.  Monitor   |
|                                       | - Deployment_                    | purposely omits Index.  Monitor types:                  |
|                                       |                                  |                                                         |
|                                       |                                  | - TCP default                                           |
+---------------------------------------+----------------------------------+---------------------------------------------------------+
| test_pools.json_                      | - HTTP 200                       | LTM Virtual Server, Monitor, Pool & Pool Member         |
|                                       | - Deployment_                    | creation.                                               |
|                                       |                                  |                                                         |
|                                       |                                  | Virtual Server:                                         |
|                                       |                                  |                                                         |
|                                       |                                  | - Address requested plus one?                           |
|                                       |                                  |                                                         |
|                                       |                                  | Monitor types:                                          |
|                                       |                                  |                                                         |
|                                       |                                  | - TCP default                                           |
|                                       |                                  | - HTTP default                                          |
|                                       |                                  |                                                         |
|                                       |                                  | Pools:                                                  |
|                                       |                                  |                                                         |
|                                       |                                  | - Default-named round robin w/ 3 members: 1 negative    |
|                                       |                                  |   and 1 duplicate                                       |
|                                       |                                  | - Explicit-named least connections w/ 13 members and    |
|                                       |                                  |   min of 2 active: 7 pre-existing by ref, 1 compound,   |
|                                       |                                  |   3 FQDN and 1 duplicate                                |
|                                       |                                  | - Explicit-named round robin w/ 2 members: many         |
|                                       |                                  |   duplicates and AdvOptions employed                    |
+---------------------------------------+----------------------------------+-------------------+-------------------------------------+
| test_pools_2.json_                    | - HTTP 200                       | coming soon                                             |
|                                       | - Deployment_                    |                                                         |
+---------------------------------------+----------------------------------+---------------------------------------------------------+
| test_pools_3.json_                    | - HTTP 200                       | coming soon                                             |
|                                       | - Deployment_                    |                                                         |
+---------------------------------------+----------------------------------+---------------------------------------------------------+
| test_pools_4.json_                    | - HTTP 200                       | coming soon                                             |
|                                       | - Deployment_                    |                                                         |
+---------------------------------------+----------------------------------+---------------------------------------------------------+
| test_pools_fixup.json_                | - HTTP 200                       | coming soon                                             |
|                                       | - Deployment_                    |                                                         |
+---------------------------------------+----------------------------------+---------------------------------------------------------+
| test_pools_fixup_2.json_              | - HTTP 200                       | coming soon                                             |
|                                       | - Deployment_                    |                                                         |
+---------------------------------------+----------------------------------+---------------------------------------------------------+
| test_pools_fixup_3.json_              | - HTTP 200                       | coming soon                                             |
|                                       | - Deployment_                    |                                                         |
+---------------------------------------+----------------------------------+---------------------------------------------------------+
| test_pools_fixup_4.json_              | - HTTP 200                       | coming soon                                             |
|                                       | - Deployment_                    |                                                         |
+---------------------------------------+----------------------------------+---------------------------------------------------------+
| test_pools_noindex.json_              | - HTTP 200                       | coming soon                                             |
|                                       | - Deployment_                    |                                                         |
+---------------------------------------+----------------------------------+---------------------------------------------------------+
| test_vs_fasthttp_tcp.json_            | - HTTP 200                       | coming soon                                             |
|                                       | - Deployment_                    |                                                         |
+---------------------------------------+----------------------------------+---------------------------------------------------------+
| test_vs_fastl4_tcp.json_              | - HTTP 200                       | coming soon                                             |
|                                       | - Deployment_                    |                                                         |
+---------------------------------------+----------------------------------+---------------------------------------------------------+
| test_vs_fastl4_udp.json_              | - HTTP 200                       | coming soon                                             |
|                                       | - Deployment_                    |                                                         |
+---------------------------------------+----------------------------------+---------------------------------------------------------+
| test_vs_ipforward.json_               | - HTTP 200                       | coming soon                                             |
|                                       | - Deployment_                    |                                                         |
+---------------------------------------+----------------------------------+---------------------------------------------------------+
| test_vs_ipforward_emptypool.json_     | - HTTP 200                       | coming soon                                             |
|                                       | - Deployment_                    |                                                         |
+---------------------------------------+----------------------------------+---------------------------------------------------------+
| test_vs_ipother.json_                 | - HTTP 200                       | coming soon                                             |
|                                       | - Deployment_                    |                                                         |
+---------------------------------------+----------------------------------+---------------------------------------------------------+
| test_vs_sctp.json_                    | - HTTP 200                       | coming soon                                             |
|                                       | - Deployment_                    |                                                         |
+---------------------------------------+----------------------------------+---------------------------------------------------------+
| test_vs_standard_http.json_           | - HTTP 200                       | coming soon                                             |
|                                       | - Deployment_                    |                                                         |
+---------------------------------------+----------------------------------+---------------------------------------------------------+
| test_vs_standard_http_afm.json_       | - HTTP 200                       | coming soon                                             |
|                                       | - Deployment_                    |                                                         |
+---------------------------------------+----------------------------------+---------------------------------------------------------+
| test_vs_standard_http_autoxff.json_   | - HTTP 200                       | coming soon                                             |
|                                       | - Deployment_                    |                                                         |
+-----------------------------------------------------+--------------------+---------------------------------------------------------+
| test_vs_standard_http_bundle_irule.json_            | - HTTP 200         | coming soon                                             |
|                                                     | - Deployment_      |                                                         |
+-----------------------------------------------------+--------------------+---------------------------------------------------------+

.. _Deployment: https://devcentral.f5.com/wiki/iApp.AppSvcsiApp_execflow.ashx#determining-success-failure-of-deployment
.. _test_monitors.json: test_monitors.json
.. _test_monitors_noindex.json: test_monitors_noindex.json
.. _test_pools.json: test_pools.json
.. _test_pools_2.json: test_pools_2.json
.. _test_pools_3.json: test_pools_3.json
.. _test_pools_4.json: test_pools_4.json
.. _test_pools_fixup.json: test_pools_fixup.json
.. _test_pools_fixup_2.json: test_pools_fixup_2.json
.. _test_pools_fixup_3.json: test_pools_fixup_3.json
.. _test_pools_fixup_4.json: test_pools_fixup_4.json
.. _test_pools_noindex.json: test_pools_noindex.json
.. _test_vs_fasthttp_tcp.json: test_vs_fasthttp_tcp.json
.. _test_vs_fastl4_tcp.json: test_vs_fastl4_tcp.json
.. _test_vs_fastl4_udp.json: test_vs_fastl4_udp.json
.. _test_vs_ipforward.json: test_vs_ipforward.json
.. _test_vs_ipforward_emptypool.json: test_vs_ipforward_emptypool.json
.. _test_vs_ipother.json: test_vs_ipother.json
.. _test_vs_sctp.json: test_vs_sctp.json
.. _test_vs_standard_http.json: test_vs_standard_http.json
.. _test_vs_standard_http_afm.json: test_vs_standard_http_afm.json
.. _test_vs_standard_http_autoxff.json: test_vs_standard_http_autoxff.json
.. _test_vs_standard_http_bundle_irule.json: test_vs_standard_http_bundle_irule.json


iWorkflow

+---------------------------------------+----------------------------------+---------------------------------------------------------+
| Test Case                             | Success Criteria                 | Summary                                                 |
+=======================================+==================================+=========================================================+
| coming soon                           |                                  |                                                         |
+---------------------------------------+----------------------------------+---------------------------------------------------------+

Contributing
------------

See `Contributing <https://github.com/F5Networks/f5-application-services-integration-iApp/blob/release/v2.0.002/CONTRIBUTING.md>`_ for information on how to contribute and expectations around test coverage in contributions.
