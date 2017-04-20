.. _iWorkflow_json_payloads_v2.0.003.zip: https://github.com/F5Networks/f5-application-services-integration-iApp/releases/download/untagged-faf6e7fb3e376026bcc0/iWorkflow_json_payloads_v2.0.003.zip

.. _iwf_doc:

How to use App Services iApp with iWorkflow
===========================================

For your convenience we've created a ZIP file containing the JSON payloads that you will need to run service templates on iWorkflow.

These file can downloaded from here: iWorkflow_json_payloads_v2.0.003.zip_.

Here are steps to use the App Services iApp with iWorkflow:

1. Download the F5 supported version of iWorkflow_appsvcs_integration_v2.0.003.json from F5 GitHub: ``https://github.com/F5Networks/f5-application-services-integration-iApp/releases``

2. Import the iApp to iWorkFlow by posting iWorkflow_appsvcs_integration_v2.0.003.json to the ``https://{{iwf_mgmt}}/mgmt/cm/cloud/templates/iapp`` endpoint (Detailed instructions: ``https://devcentral.f5.com/wiki/iWorkflow.HowToSamples_importing_iapp_templates_to_iworkflow.ashx``)

3. Discover a new BIG-IP device in iWorkFlow GUI if you don’t have any (Detailed instructions:  ``https://devcentral.f5.com/wiki/iWorkflow.HowToSamples_programming_bigip_device_discovery.ashx``)

4. Create a local connector following instructions provided here: ``https://devcentral.f5.com/wiki/iWorkflow.APIRef_cm_cloud_connectors_local.ashx#create-connector-cloud``

5. Create a tenant user with LDAP provider or Active Directory provider (Detailed instructions: ``https://devcentral.f5.com/wiki/iWorkflow.HowToSamples_iworkflow_tenant_create.ashx``)

6. For tenant convenience, we provide service templates that cover most popular use cases:

  * f5-fasthttp-lb_v2.0.003.json
  * f5-fastl4-tcp-lb_v2.0.003.json
  * f5-fastl4-udp-lb_v2.0.003.json
  * f5-http-lb_v2.0.003.json
  * f5-http-url-routing-lb_v2.0.003.json
  * f5-https-offload_v2.0.003.json
  * f5-https-waf-lb_v2.0.003.json

  To upload service templates iWorkflow Administrator should send them by POST method to ``https://{{iwf_mgmt}}/mgmt/cm/cloud/provider/templates/iapp``

  If you want to create your own JSON service template please read this document: ``https://devcentral.f5.com/wiki/iWorkflow.HowToSamples_programming_provider_template_add.ashx``

7. Create service using one of provided in step 6 JSON service templates or your own. (Detailed instructions: ``https://devcentral.f5.com/wiki/iWorkflow.HowToSamples_iworkflow_tenant_service_create.ashx``)

  Alternatively, you can also use service that we built for you based on JSON service templates from step 6:
  
  * f5-fasthttp-lb-service_v2.0.003.json
  * f5-fastl4-tcp-lb-service_v2.0.003.json
  * f5-fastl4-udp-lb-service_v2.0.003.json
  * f5-http-lb-service_v2.0.003.json
  * f5-http-url-routing-lb-service_v2.0.003.json
  * f5-https-offload-service_v2.0.003.json
  * f5-https-waf-lb-service_v2.0.003.json
    
  To upload particular service POST the \*.service.json file to ``https://{{iwf_mgmt}}/mgmt/cm/cloud/tenants/{{iwf_tenant_name}}/services/iapp`` as authenticated tenant user (basic auth or f5-token) that was created in step  5.

  In your \*.service.json change placeholders { eg. {{appsvcs_vip_addr}} to values from your environment.

  To create asm policy for f5-https-waf-lb-service_v2.0.003.json POST the payload described below to ``https://{{bigip_mgmt}}/mgmt/tm/util/bash``::

    {
      "command":"run",
      "utilCmdArgs":"-c 'tmsh create asm policy /Common/{{policy_name}} active encoding utf-8 policy-builder enabled'"
    }

User Guide for App Services iApp: ``https://devcentral.f5.com/wiki/iApp.AppSvcsiApp_userguide_userguide.ashx``
