#!/usr/bin/env python

import ipaddress
import requests
import sys
import logging
import glob
import json
import paramiko
import os
from requests.exceptions import ConnectionError
from requests.packages.urllib3.exceptions import InsecureRequestWarning


def fix_indents(path):
    for filename in glob.glob(path):
        with open(filename, 'r') as template:
            json_content = json.load(template)

        with open(filename, 'w+') as template:
            json.dump(json_content, template, indent=4, sort_keys=True)


class IPAddressGenerator(object):
    def __init__(self, network):
        self._network = network
        self._hosts = list(reversed(list(self._network.hosts())))

    def get_next(self):
        return self._hosts.pop()

    def get_last(self):
        hosts = list(reversed(self._hosts))
        last = hosts.pop()
        self._hosts = list(reversed(hosts))
        return last

    def get_network_address(self):
        return self._network.network_address


class IPv4AddressGenerator(IPAddressGenerator):
    def __init__(self, network_str):
        super(IPv4AddressGenerator, self).__init__(
            ipaddress.IPv4Network(network_str))


class IPv6AddressGenerator(IPAddressGenerator):
    def __init__(self, network_str):
        super(IPv6AddressGenerator, self).__init__(
            ipaddress.IPv6Network(network_str))


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

        self._bash_url = "https://{}/mgmt/tm/util/bash".format(host)
        self._app_url = "https://{}/mgmt/tm/sys/application/service".format(
            host)
        self._version_url = "https://{}/mgmt/tm/sys/software/volume?" \
                            "$select=active,version".format(host)

    def _get_session(self):
        requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
        session = requests.session()
        session.auth = (self._username, self._password)
        session.verify = False

        return session

    def get_version(self):
        session = self._get_session()
        resp = session.get(self._version_url)

        if resp.status_code == 401:
            logging.error("Authentication to {} failed".format(self._host))
            sys.exit(1)

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
