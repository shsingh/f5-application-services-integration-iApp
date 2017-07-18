#!/usr/bin/env python
import json
import time

import paramiko
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning


class BIPClient(object):
    def __init__(self, host, logging, ssh_port=22,
                 username='admin', password='admin',
                 ssh_username='root', ssh_password='default'):

        self._host = host
        self._ssh_port = ssh_port
        self._username = username
        self._password = password
        self._ssh_username = ssh_username
        self._ssh_password = ssh_password
        self._logging = logging

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

    def app_services_deployed(
            self, payload, no_check=False, max_check=10, wait=5):
        if no_check:
            return True

        current_time = int(time.time())
        istat_key = self._get_istat_key(payload['partition'], payload['name'])
        command = 'tmsh run cli script appsvcs_get_istat \"{}\"'.format(
            istat_key)

        for check_run in range(max_check):
            self._logging.info("checking for deployment completion ({}/{})".format(
                check_run, max_check))
            stdout = self.run_command(command)
            self._logging.debug("[check_deploy] current_time={} result={}".format(
                current_time, stdout))

            if stdout.startswith("FINISHED_"):
                parts = stdout.split('_')
                fin_time = int(parts[1])
                if fin_time > current_time:
                    return True

            time.sleep(wait)

        return False

    def app_services_exists(self, partition, name):
        session = self._get_session()
        url = self._get_app_services_existence_url(
            self._app_url,
            partition,
            name
        )
        result = session.get(url)
        if result.status_code == 200:
            return True
        elif result.status_code == 404:
            return False
        else:
            raise Exception(result)

    def deploy_app_service(self, payload):
        session = self._get_session()
        if not self.app_services_exists(payload['partition'], payload['name']):
            session.post(self._app_url, data=json.dumps(payload))

        return self.app_services_deployed(payload)

    def remove_app_service(self, payload):
        session = self._get_session()
        response = session.delete(self._get_app_services_existence_url(
            self._app_url,
            payload['partition'],
            payload['name']
        ))

        if response.status_code == requests.codes.ok:
            self._logging.info("Application service \"{}\" removed".format(
                payload['name']))
            return True
        else:
            self._logging.error("Delete failed: {}".format(response.json()))
            return False

    def get_version(self):
        session = self._get_session()
        resp = session.get(self._version_url)

        if resp.status_code == 401:
            msg = "Authentication to {} failed".format(self._host)
            self._logging.error(msg)
            raise Exception(msg)

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
                self._logging.debug(
                    "[template_list] found template named {}".format(
                        item["name"]))
                result.append(item["name"])

        result.sort()

        return result.pop()

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
        stdin.flush()
        client.close()
        return out
