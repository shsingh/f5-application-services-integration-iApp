#!/usr/bin/env python
import json


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


class RESTException(Exception):
    def __init__(self, rest_json):
        msg = "REST interface said:\n{}".format(
            json.dumps(rest_json, indent=4, sort_keys=True))

        super(RESTException, self).__init__(msg)
