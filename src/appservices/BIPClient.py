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
import os
import re
import time
import getpass

import paramiko
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

from src.appservices.exceptions import AppServiceDeploymentException
from src.appservices.exceptions import AppServiceDeploymentVerificationException
from src.appservices.exceptions import AppServiceRemovalException
from src.appservices.exceptions import RESTException
from src.appservices.tools import mk_dir
from paramiko.ssh_exception import PasswordRequiredException


class BIPClient(object):
    def __init__(self, host, ssh_port=22,
                 username='admin', password='admin',
                 ssh_username='root', ssh_password='default', logger=None):

        self._host = host
        self._ssh_port = ssh_port
        self._username = username
        self._password = password
        self._ssh_username = ssh_username
        self._ssh_password = ssh_password
        self._ssh_key_password = None

        if logger is None:
            self._logger = logging.getLogger(__name__)
        else:
            self._logger = logger

        self._url_app = "https://{}/mgmt/tm/sys/application/service".format(
            host)
        self._url_version = "https://{}/mgmt/tm/sys/software/volume?" \
                            "$select=active,version".format(host)
        self._url_template = "https://{}/" \
                             "mgmt/tm/sys/application/template".format(host)
        self._url_app_template = "{}?$select=name".format(self._url_template)
        self._url_save_cfg = "https://{}/mgmt/tm/sys/config".format(host)
        self._url_cli_script = "https://{}/mgmt/tm/cli/script".format(host)

    def _get_session(self):
        requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
        session = requests.session()
        session.auth = (self._username, self._password)
        session.verify = False

        return session

    @staticmethod
    def _get_istat_key(partition, name):
        return "sys.application.service " \
               "/{0}/{1}.app/{1} string deploy.postdeploy_final".format(
            partition, name)

    def _url_app_service_exists(self, partition, name):
        return "{0}/~{1}~{2}.app~{2}".format(
            self._url_app, partition, name)

    def _url_template_exits(self, name):
        return "{}/{}".format(self._url_template, name)

    def _url_definition(self, name):
        return "{}/actions/definition".format(
            self._url_template_exits(name))

    def _url_cli_exists(self, name):
        return "{}/{}".format(self._url_cli_script, name)

    def handle_response(self, response):
        if response.status_code == 200:
            # self._logger.debug(response.json())
            return True
        elif response.status_code == 404:
            self._logger.warn(response.json())
            return False
        elif response.status_code == 401:
            self._logger.error("Login/Password incorrect")
            return False

        raise RESTException(response.json())

    def cli_script_exists(self, name):
        session = self._get_session()
        return self.handle_response(
            session.get(self._url_cli_exists(name))
        )

    def deploy_cli_script(self, payload):
        session = self._get_session()
        return self.handle_response(
            session.post(self._url_cli_script, data=json.dumps(payload))
        )

    def update_cli_script(self, name, payload):
        session = self._get_session()
        return self.handle_response(
            session.put(self._url_cli_exists(name), data=json.dumps(payload))
        )

    def check_if_template_exists(self, name):
        session = self._get_session()
        return self.handle_response(
            session.get(self._url_template_exits(name))
        )

    def deploy_template(self, payload):
        session = self._get_session()
        return self.handle_response(
            session.post(self._url_template, data=json.dumps(payload))
        )

    def update_template(self, name, payload):
        session = self._get_session()
        return self.handle_response(
            session.put(
                self._url_template_exits(name),
                data=json.dumps(payload)
            )
        )

    def update_template_definition(self, name, payload):
        session = self._get_session()
        return self.handle_response(
            session.put(
                self._url_definition(name),
                data=json.dumps(payload)
            )
        )

    def verify_deployment(
            self, payload, no_check=False, max_check=10, wait=6):
        if no_check:
            return True

        current_time = int(time.time())
        istat_key = self._get_istat_key(payload['partition'], payload['name'])
        command = 'istats get \"{}\"'.format(
            istat_key)

        for check_run in range(max_check):
            self._logger.info(
                "checking for deployment completion ({}/{}) of {}".format(
                    check_run, max_check, payload['name']))
            stdout, _ = self.run_command(command)
            self._logger.debug(
                "[check_deploy] current_time={} result={}".format(
                    current_time, stdout))

            if stdout.startswith("FINISHED_"):
                parts = stdout.split('_')
                fin_time = int(parts[1])
                if fin_time > current_time:
                    self._logger.info(
                        "BigIP returned expected timestamp "
                        "for deployment of {}".format(payload['name']))
                    return True

            time.sleep(wait)

        raise AppServiceDeploymentException(payload['name'], stdout)

    def save_config(self):
        payload = {"command": "save"}
        session = self._get_session()
        return self.handle_response(
            session.post(self._url_save_cfg, data=json.dumps(payload))
        )

    def app_services_exists(self, partition, name):
        session = self._get_session()
        url = self._url_app_service_exists(
            partition,
            name
        )
        return self.handle_response(
            session.get(url)
        )

    def verify_deployment_result(self, payload, log_dir):
        stdout, stderr = self.run_command(
            "tmsh -c 'cd /{}/{}.app ; list ltm ; list asm ; list apm'".format(
                payload['partition'], payload['name']))

        mk_dir(log_dir)
        with open(os.path.join(
                log_dir, 'deployment_result.txt'), 'w') as log_file:
            log_file.write("{}\n".format(stderr))
            log_file.write("{}\n".format("-"*60))
            log_file.write(stdout)

        if stderr != '':
            raise AppServiceDeploymentVerificationException(
                payload['name'], stderr)

        return True

    def deploy_app_service(self, payload):
        session = self._get_session()
        try:
            if not self.app_services_exists(
                    payload['partition'], payload['name']):
                self.handle_response(
                    session.post(self._url_app, data=json.dumps(payload))
                )
            else:
                # OMG! hacking payload for redeploy
                try:
                    del payload["inheritedDevicegroup"]
                    del payload["inheritedTrafficGroup"]
                    del payload["deviceGroup"]
                    del payload["trafficGroup"]
                    payload["execute-action"] = "definition"
                except KeyError as ex:
                    self._logger.exception(ex)

                self.handle_response(
                    session.put(
                        self._url_app_service_exists(
                            payload['partition'],
                            payload['name']),
                        data=json.dumps(payload)
                    )
                )

        except RESTException:
            self._logger.exception("Deployment of {} failed".format(
                payload['name']))
            raise

        try:
            return self.verify_deployment(payload)
        except AppServiceDeploymentException:
            self._logger.exception("Deployment verification of"
                                   " {} failed".format(payload['name']))
            raise

    def remove_app_service(self, payload):
        session = self._get_session()
        response = session.delete(
            self._url_app_service_exists(
                payload['partition'],
                payload['name']))

        if response.status_code == 200:
            self._logger.info("Application service \"{}\" removed".format(
                payload['name']))
            return True
        else:
            raise AppServiceRemovalException(payload['name'], response.json())

    def get_version(self):
        session = self._get_session()
        resp = session.get(self._url_version)

        if resp.status_code == 401:
            raise RESTException(resp.json())

        if resp.status_code == 200:
            for item in resp.json()["items"]:
                if 'active' in item.keys() and item["active"]:
                    version = item["version"]
                    parts = version.split('.')

                    return {
                        'version': '_'.join(parts),
                        'major': '_'.join(parts[0:-1]),
                        'minor': parts[2]
                    }
        return {}

    def get_template_name(self):
        session = self._get_session()
        resp = session.get(self._url_app_template)
        templates = resp.json()

        result = []
        for item in templates["items"]:
            if item["name"].startswith("appsvcs_integration_"):
                self._logger.debug(
                    "[template_list] found template named {}".format(
                        item["name"]))
                result.append(item["name"])

        result.sort()

        try:
            return result.pop()
        except IndexError as ex:
            self._logger.exception(ex)
            self._logger.error("App Services template"
                               " was not installed on {}".format(self._host))

    def download_logs(self, log_folder, bip_log_files=None):
        if bip_log_files is None:
            bip_log_files = [
                '/var/log/restjavad.0.log',
                '/var/log/ltm',
                '/var/log/icrd',
                '/var/tmp/scriptd.out'
            ]
        mk_dir(log_folder)
        self.download_files(bip_log_files, log_folder)

    def download_qkview(self, log_folder):
        result, error = self.run_command("qkview -c")
        # for some reason qkview outputs this data on stderr
        # error = "Gathering System Diagnostics: Please wait ... " \
        #         "Diagnostic information has been saved in: " \
        #         "/var/tmp/test-BIGIP-11.6.1_1.example.com.qkview" \
        #         "Please send this file to F5 support."
        pattern = re.compile("([a-zA-Z0-9\.\-_/]+\.qkview)")
        file_path = pattern.findall(error)
        self.download_files(file_path, log_folder)
        return os.path.basename(file_path[0])

    def get_private_key(self):
        file_path = os.path.join(os.path.expanduser("~"), ".ssh/id_rsa")

        try:
            return paramiko.RSAKey.from_private_key_file(file_path)
        except PasswordRequiredException as ex:
            self._logger.error(ex)

            self._logger.warn("Your ssh key is encrypted, please enter the decryption password")

            if not self._ssh_key_password:
                self._ssh_key_password = getpass.getpass()

            return paramiko.RSAKey.from_private_key_file(file_path, self._ssh_key_password)

        except IOError:
            return

    def download_files(self, files, log_folder):
        client = paramiko.Transport((self._host, self._ssh_port))
        client.connect(username=self._ssh_username, password=self._ssh_password)
        sftp = paramiko.SFTPClient.from_transport(client)
        for log_file in files:
            sftp.get(log_file, os.path.join(
                log_folder,
                os.path.basename(log_file)))
        client.close()

    def upload_files(self, local_files, remote_files):
        client = paramiko.Transport((self._host, self._ssh_port))
        client.connect(username=self._ssh_username, password=self._ssh_password)
        sftp = paramiko.SFTPClient.from_transport(client)
        for local_file, remote_file in zip(local_files, remote_files):
            sftp.put(local_file, remote_file)
        client.close()

    def run_command(self, command):
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(self._host, self._ssh_port,
                       self._ssh_username, self._ssh_password,
                       compress=True, look_for_keys=False)
        stdin, stdout, stderr = client.exec_command(command)
        out = stdout.read().strip()
        err = stderr.read().strip()
        stdin.flush()
        client.close()
        return out, err
