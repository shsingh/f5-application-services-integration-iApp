:github_url: https://github.com/F5Networks/f5-application-services-integration-iApp/docs

.. _iApp: https://devcentral.f5.com/wiki/iApp.HomePage.ashx
.. _F5 Networks: https://www.f5.com
.. _SOL80012344: https://support.f5.com/kb/en-us/solutions/public/k/80/sol80012344.html
.. _ASK F5: http://askf5.com
.. _Guideline Policies: http://www.f5.com/about/guidelines-policies/

.. toctree::
	:hidden:
	:maxdepth: 3	

	overview
	userguide/userguide
	refguide

App Services Integration iApp
=============================

Release Version: |release|

Introduction
------------

The purpose of this project is to provide an iApp_ template that can be used to 
automate and orchestrate Layer 4-7 applications service deployments using 
`F5 Networks`_ BIG-IP/iWorkflow Products.  Additionally, this template serves as
a common integration point for third party SDN/NFV/Automation/Orchestration 
products.

Support
-------

Maintenance and F5 Technical Support of the F5 code is provided only if the software (i) is unmodified; and (ii) has been marked as F5 Supported in `SOL80012344`_. Support will only be provided to customers who have an existing support contract, purchased separately, subject to F5’s support policies available at `Guideline Policies`_ and `ASK F5`_.

.. _testedversions:

Tested Versions
---------------

We currently test against the following versions of the F5 BIG-IP TMOS:

- 11.5.3 HF2 Build: 2.0.196
- 11.5.4 HF2 Build: 2.0.291
- 11.6.0 HF8 Build: 8.0.482
- 11.6.1 HF1 Build: 1.0.326
- 12.0.0 HF4 Build: 4.0.674
- 12.1.0 HF2 Build: 2.0.1468
- 12.1.1 HF1 Build: 1.0.196

and IWF 2.1.0 service catalog, Big-IP 12.1 with local cloud connector on the following feature collections (Service Template JSON files):

- f5-https-offload_v2.0.003
- f5-http-lb_v2.0.003
- f5-fastl4-tcp-lb_v2.0.003
- f5-fastl4-udp-lb_v2.0.003
- f5-fasthttp-lb_v2.0.003
- f5-http-url-routing-lb_v2.0.003
- f5-https-waf-lb_v2.0.003

Getting Started
---------------

To get started head over to the :doc:`userguide/userguide`.  Advanced users 
should also read the :doc:`refguide`

Learn :ref:`iwf_doc`
