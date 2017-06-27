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

.. _Documentation: https://devcentral.f5.com/wiki/iApp.AppSvcsiApp_userguide_module4_lab3.ashx

Introduction
------------

Explanation of test automation for BIG-IP and iWorkflow.

Documentation
-------------

Please refer to the F5 App Services Integration iApp `project documentation <https://devcentral.f5.com/wiki/iApp.AppSvcsiApp_userguide_module4_lab3.ashx>`_ for detailed information.

Test Cases
----------

BIG-IP

+---------------------------------------+----------------------------------+---------------------------------------------------------+
| Test Case                             | Success Criteria                 | Summary                                                 |
+=======================================+==================================+=========================================================+
| test_monitors.json_                   | - HTTP 200                       | LTM Monitor Creation & Utilize in LTM Pool. Monitor     |
|                                       | - Deployment_                    | types:                                                  |
|                                       |                                  |                                                         |
|                                       |                                  | - TCP default                                           |
|                                       |                                  | - HTTP default                                          |
|                                       |                                  | - HTTP custom inline                                    |
|                                       |                                  | - HTTP custom by ref                                    |
+---------------------------------------+----------------------------------+-------------------+-------------------------------------+
| test_monitors_noindex.json_           | - HTTP 200                       | LTM Monitor Creation w/o Index & Utilize in LTM Pool.   |
|                                       | - Deployment_                    | Monitor types:                                          |
|                                       |                                  |                                                         |
|                                       |                                  | - TCP default                                           |
+---------------------------------------+----------------------------------+-------------------+-------------------------------------+

.. _Deployment: https://devcentral.f5.com/wiki/iApp.AppSvcsiApp_execflow.ashx#determining-success-failure-of-deployment
.. _test_monitors.json: test_monitors.json
.. _test_monitors_noindex.json: test_monitors_noindex.json

Contributing
------------

See `Contributing <https://github.com/F5Networks/f5-application-services-integration-iApp/blob/release/v2.0.002/CONTRIBUTING.md>`_.
