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
import json
import logging


class AppServiceDeploymentException(Exception):
    def __init__(self, name, reason):
        if reason == '':
            msg = "BigIP did not provide any reason" \
                  " for failed deployment of {}".format(name)
        else:
            msg = "Deployment of {}, failed with: {}".format(name, reason)

        super(AppServiceDeploymentException, self).__init__(msg)


class AppServiceDeploymentVerificationException(Exception):
    def __init__(self, name, reason):
        msg = "Verification of deployment of {}, failed with {}".format(
            name, reason)

        super(AppServiceDeploymentVerificationException, self).__init__(msg)


class AppServiceRemovalException(Exception):
    def __init__(self, name, reason):
        msg = "Removal of deployment of {}, failed with {}".format(
            name, reason)

        super(AppServiceRemovalException, self).__init__(msg)


class ParameterMissingException(Exception):
    def __init__(self, parameter):
        msg = "Please provide required parameter {}".format(parameter)

        super(ParameterMissingException, self).__init__(msg)


class RESTException(Exception):
    def __init__(self, response):
        try:
            msg = "REST interface said:\n{}".format(
                json.dumps(response.json(), indent=4, sort_keys=True))
        except ValueError:
            msg = "REST interface did NOT return a valid JSON"
            logger = logging.getLogger(__name__)
            logger.error(msg)

        super(RESTException, self).__init__(msg)
        self._response = response

    def get_response(self):
        return self._response
