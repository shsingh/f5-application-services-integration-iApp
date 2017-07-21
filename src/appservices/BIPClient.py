#!/usr/bin/env python
import json
import time
import os

import paramiko
import requests
import logging
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from src.appservices.tools import mk_dir
from src.appservices.exceptions import AppServiceDeploymentException
from src.appservices.exceptions import RESTException
from src.appservices.exceptions import AppServiceDeploymentVerificationException
from src.appservices.exceptions import AppServiceRemovalException


class BIPClient(object):
    def __init__(self, host, ssh_port=22,
                 username='admin', password='admin',
                 ssh_username='root', ssh_password='default'):

        self._host = host
        self._ssh_port = ssh_port
        self._username = username
        self._password = password
        self._ssh_username = ssh_username
        self._ssh_password = ssh_password
        self._logger = logging.getLogger(__name__)

        self._app_url = "https://{}/mgmt/tm/sys/application/service".format(
            host)
        self._version_url = "https://{}/mgmt/tm/sys/software/volume?" \
                            "$select=active,version".format(host)
        self._app_template_url = "https://{}/mgmt/tm/sys/application/" \
                                 "template?$select=name".format(host)

    def _get_session(self):
        requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
        session = requests.session()
        session.auth = (self._username, self._password)
        session.verify = False

        return session

    @staticmethod
    def _get_app_services_existence_url(url, partition, name):
        return "{0}/~{1}~{2}.app~{2}".format(
            url, partition, name)

    @staticmethod
    def _get_istat_key(partition, name):
        return "sys.application.service " \
               "/{0}/{1}.app/{1} string deploy.postdeploy_final".format(
            partition, name)

    def verify_deployment(
            self, payload, no_check=False, max_check=10, wait=6):
        if no_check:
            return True

        current_time = int(time.time())
        istat_key = self._get_istat_key(payload['partition'], payload['name'])
        command = 'tmsh run cli script appsvcs_get_istat \"{}\"'.format(
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
                    return True

            time.sleep(wait)

        raise AppServiceDeploymentException(payload['name'], stdout)

    def app_services_exists(self, partition, name):
        session = self._get_session()
        url = self._get_app_services_existence_url(
            self._app_url,
            partition,
            name
        )
        result = session.get(url)
        if result.status_code == 200:
            self._logger.warn(result.json())
            return True
        elif result.status_code == 404:
            self._logger.info(result.json())
            return False
        else:
            raise RESTException(result.json())

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

    def deploy_app_service(self, payload):
        session = self._get_session()
        try:
            if not self.app_services_exists(payload['partition'], payload['name']):
                result = session.post(self._app_url, data=json.dumps(payload))
                if result.status_code != 200:
                    raise RESTException(result.json())

        except RESTException as e:
            self._logger.exception("Deployment of {} failed".format(
                payload['name']))
            raise

        try:
            return self.verify_deployment(payload)
        except AppServiceDeploymentException as e:
            self._logger.exception("Deployment verification of"
                                   " {} failed".format(payload['name']))
            raise

    def remove_app_service(self, payload):
        session = self._get_session()
        response = session.delete(self._get_app_services_existence_url(
            self._app_url,
            payload['partition'],
            payload['name']
        ))

        if response.status_code == requests.codes.ok:
            self._logger.info("Application service \"{}\" removed".format(
                payload['name']))
            return True
        else:
            raise AppServiceRemovalException(payload['name'], response.json())

    def get_version(self):
        session = self._get_session()
        resp = session.get(self._version_url)

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
        resp = session.get(self._app_template_url)
        templates = resp.json()

        result = []
        for item in templates["items"]:
            if item["name"].startswith("appsvcs_integration_"):
                self._logger.debug(
                    "[template_list] found template named {}".format(
                        item["name"]))
                result.append(item["name"])

        result.sort()

        return result.pop()

    def download_logs(self, log_folder):
        mk_dir(log_folder)
        self.download_files([
            '/var/log/restjavad.0.log',
            '/var/log/ltm',
            '/var/log/icrd',
            '/var/tmp/scriptd.out'
        ], log_folder)

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
