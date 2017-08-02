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

Testing
=========================================================

The App Services Integration iApp package includes pytest compatible tests.
Tests are grouped in folders
- appservices, containing unit tests
- functional, containing functional tests

Functional tests start from verifying the connection with a BigIP. Then they proceed
with a legacy tests run. The legacy test run takes the JSON templates defined in
``PROJECT_ROOT/payload_templates``, builds configuration / Application Services payloads
and POSTs those payloads to specified BigIP.
There are about 50 use cases in that folder, each one of them will be deployed and un deployed once.

The very last test is the scale test. In this case the test deploys a specified number of Application Services.
The number can be adjusted with ``--scale_size`` parameter passed to pytest.
``--scale_size=N`` will deploy N instances of an Application Service, when completed it will remove all of them.
Scale test can take about 8 hours to complete assuming that ``--scale_size`` was set to 20.

Developers interested in running the test framework would install create a python virtualenv
with dependencies defined in ``PROJECT_ROOT/requirements.txt``

To run the complete test framework the following prerequisite steps are required:

The test script currently requires unix-style utilities (scp/ssh). Linux and Mac OS have these utilities installed or available. To run the test framework on a Windows system please install Cygwin.

1. Provision your BIG-IP device with the following modules in at a ‘nominal’ level:
  - LTM
  - APM
  - ASM
  - AFM

2. Configure NTP and DNS servers on the BIG-IP system. DNS servers should be able to resolve internet host names.
3. Make sure your python virtual environment is provisioned and enabled

.. code-block:: bash

    virtualenv venv
    source venv/bin/activate
    pip install -r requirements.txt

3. Build the template using the command ``mgmt_build.py -b resources/bundled.test/``
4. Upload the template using the command ``mgmt_template.py -o -a build/iapp.apl -i build/iapp.tcl -u BIG_IP_USERNAME -p BIG_IP_PASSWORD IP_ADDRESS_OF_BIG_IP $(basename -s .tmpl build/appsvcs_integration_*)``
5. Untar ``PROJECT_ROOT/resources/remote_url_files.tar.gz`` to the root of a webserver. This server will be later referred to as the **policy host**
6. Run the tests

.. code-block:: bash

    pytest -x --policy_host=IP_ADDRESS_OF_POLICY_HOST_SERVER --host=IP_ADDRESS_OF_BIG_IP --scale_size=NUMBER_OF_IAPPS_DEPLOYED_DURING_SCALE_RUN

example:

.. code-block:: bash

    pytest -x --policy_host=10.0.0.1 --host=10.0.0.2 --scale_size=20

7. Monitor the tests run by running ``tail -f PROJECT_ROOT/logs/application_services_integration.log``
8. In case of failure the runner will download a \*.qkview and other logs into ``PROJECT_ROOT/logs/**`` folder


If you are running our functional tests you will need a real BIG-IP® to run them against, but you can get one of those pretty easily in
 [Amazon EC2](https://aws.amazon.com/marketplace/pp/B00JL3UASY/ref=srh_res_product_title?ie=UTF8&sr=0-10&qid=1449332167461).
