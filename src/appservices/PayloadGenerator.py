#!/usr/bin/env python

import os
import re
import random
import json
import logging
from tools import IPv4AddressGenerator
from tools import IPv6AddressGenerator
from tools import save_json
from tools import mk_dir


class PayloadGenerator(object):
    def __init__(self,
                 base_dir,
                 template_dir='payload_templates',
                 payloads_dir='payloads',
                 tmp_dir='tmp'):
        self._base_dir = os.path.abspath(base_dir)
        self._template_dir = os.path.abspath(template_dir)
        self._payloads_dir = os.path.abspath(payloads_dir)
        self._tmp_dir = os.path.abspath(tmp_dir)

    def get_tmp_dir(self):
        return self._tmp_dir

    def fill_template(
            self, abs_template_path, session_id, version, policy_host,
            server_v4_network, server_v6_network,
            server_first_v4_address, server_first_v6_address,
            pull_v4_network, pull_v6_network,
            pull_first_v4_address, pull_first_v6_address):

        server_v4_gen = IPv4AddressGenerator(
            server_v4_network, server_first_v4_address)
        server_v6_gen = IPv6AddressGenerator(
            server_v6_network, server_first_v6_address)
        pull_v4_gen = IPv4AddressGenerator(
            pull_v4_network, pull_first_v4_address)
        pull_v6_gen = IPv6AddressGenerator(
            pull_v6_network, pull_first_v6_address)

        result = [False, "", "Common"]

        tmp_file_name = os.path.basename(abs_template_path)

        mk_dir(self._tmp_dir)

        with open(abs_template_path, 'r') as template:
            with open(os.path.join(
                self._tmp_dir,
                "{}.{}.tmp".format(tmp_file_name, session_id)
            ), "wt") as tmp:
                for line in template:
                    line = re.sub(
                        r'\%TEST_NAME\%', tmp_file_name.split('.')[0], line)
                    vs_ip_match = re.match(
                        r'.*%TEST_VS_IP%.*', line)
                    vs6_ip_match = re.match(
                        r'.*%TEST_VS6_IP%.*', line)
                    member_ip_match = re.match(
                        r'.*%TEST_MEMBER_IP%.*', line)
                    member6_ip_match = re.match(
                        r'.*%TEST_MEMBER6_IP%.*', line)
                    snat_ip_match = re.match(
                        r'.*%TEST_RANGE_(\d)_IP%.*', line)
                    snat6_ip_match = re.match(
                        r'.*%TEST_RANGE6_(\d)_IP%.*', line)
                    version_match = re.match(
                        r'.*%TEST_DEV_VERSION_(.*)%.*', line)
                    delete_override_match = re.match(
                        r'.*\"test_delete_override\":\"true\".*', line)
                    parent_match = re.match(
                        r'.*\"test_parent\":\"(.*)\".*', line)
                    partition_match = re.match(
                        r'.*\"partition\":\"(.*)\".*', line)
                    policyhost_match = re.match(
                        r'.*%TEST_POLICY_HOST%.*', line)
                    random_match = re.match(
                        r'.*%RANDOM%.*', line)

                    if random_match:
                        line = re.sub(
                            r'\%RANDOM\%',
                            str(random.randint(10000, 99999)), line)

                    if partition_match:
                        result[2] = partition_match.group(1)

                    if parent_match:
                        result[1] = parent_match.group(1)

                    if policyhost_match:
                        line = re.sub(r'\%TEST_POLICY_HOST\%',
                                      policy_host, line)

                    if delete_override_match:
                        result[0] = True

                    if version_match:
                        if version_match.group(1) == "MAJOR":
                            line = re.sub(r'\%TEST_DEV_VERSION_MAJOR\%',
                                          version["major"], line)

                        if version_match.group(1) == "MINOR":
                            line = re.sub(r'\%TEST_DEV_VERSION_MINOR\%',
                                          version["minor"], line)

                        if version_match.group(1) == "FULL":
                            line = re.sub(r'\%TEST_DEV_VERSION_FULL\%',
                                          version["version"], line)

                    if vs_ip_match:
                        line = re.sub(r'\%TEST_VS_IP\%',
                                      "{}".format(
                                          str(server_v4_gen.get_next())), line)

                    if vs6_ip_match:
                        line = re.sub(r'\%TEST_VS6_IP\%',
                                      "{}".format(
                                          str(server_v6_gen.get_next())), line)

                    if member_ip_match:
                        line = re.sub(r'\%TEST_MEMBER_IP\%',
                                      "{}".format(
                                          str(pull_v4_gen.get_next())
                                      ), line)

                    if member6_ip_match:
                        line = re.sub(r'\%TEST_MEMBER6_IP\%',
                                      "{}".format(
                                          str(pull_v6_gen.get_next())), line)

                    if snat_ip_match:
                        snat_ips = []
                        for sip in range(int(snat_ip_match.group(1))):
                            snat_ips.append(str(pull_v4_gen.get_last()))
                        line = re.sub(r'\%TEST_RANGE_[\d]_IP\%',
                                      "{}".format(','.join(snat_ips)), line)

                    if snat6_ip_match:
                        snat6_ips = []
                        for s6ip in range(int(snat6_ip_match.group(1))):
                            snat6_ips.append(str(pull_v6_gen.get_last()))
                        line = re.sub(r'\%TEST_RANGE6_[\d]_IP\%',
                                      "{}".format(','.join(snat6_ips)), line)

                    tmp.write(line)

        return result

    @staticmethod
    def read_template(template_path):
        try:
            template_file = open(template_path)
            content = json.load(template_file)
            template_file.close()
            return content
        except (IOError, ValueError, NameError) as error:
            raise error

    @staticmethod
    def validate_template(template):
        required_fields = [
            'name', 'template_name', 'partition', 'username', 'password',
            'inheritedDevicegroup', 'inheritedTrafficGroup', 'deviceGroup',
            'trafficGroup']
        for field in required_fields:
            if field not in template:
                msg = "The required key \"{}\" was not found in" \
                      " the JSON template (or it's parent(s))".format(field)
                raise Exception(msg)

    @staticmethod
    def _append_credentials(tmpl, username=None, password=None,
                            password_file=None):
        if username is not None:
            if 'username' in tmpl:
                logging.info("Username found in JSON but specified on CLI,"
                             "using CLI value")
            tmpl["username"] = username

        if password is not None:
            if 'password' in tmpl:
                logging.info("Password found in JSON but specified on CLI,"
                             "using CLI value")
            tmpl["password"] = password
        if password_file is not None:
            if 'password' in tmpl:
                logging.info("Password found in JSON but specified in CLI,"
                             " using CLI value")
            with open(password_file, 'r') as p_file:
                tmpl["password"] = p_file.readline().strip()

        return tmpl

    def build_template(self, template_dir, template_file_name,
                       username=None, password=None, password_file=None):
        tmpl = self.read_template(
            os.path.join(template_dir, template_file_name))
        flat_tmpl = self.flatten_template(tmpl['parent'], tmpl, template_dir)

        flat_tmpl = self._append_credentials(
            flat_tmpl, username, password, password_file)

        self.validate_template(flat_tmpl)

        return flat_tmpl

    @staticmethod
    def update_app_services_name(tmpl, name):
        logging.debug("[template_select] specified={}".format(
            tmpl["template_name"]))
        if tmpl["template_name"] == "latest":
            tmpl["template_name"] = name
            logging.debug("[template_select] selected={}".format(
                tmpl["template_name"]))
        else:
            if tmpl["template_name"] not in tmpl:
                msg = "iApp template \"{}\"" \
                      " is not installed on BIG-IP".format(
                    tmpl["template_name"])
                raise Exception(msg)

        return tmpl

    def build_payload(self, template, app_name,
                      payload_filename=None, payload_directory=None):

        template = self.update_app_services_name(template, app_name)

        deploy_payload = {
            "inheritedDevicegroup": template["inheritedDevicegroup"],
            "inheritedTrafficGroup": template["inheritedTrafficGroup"],
            "deviceGroup": template["deviceGroup"],
            "trafficGroup": template["trafficGroup"],
            "template": template["template_name"],
            "partition": template["partition"],
            "name": template["name"],
            "variables": [],
            "tables": [],
            "lists": []
        }

        for string in template["strings"]:
            k, v = string.popitem()
            deploy_payload["variables"].append(
                {"name": k, "value": v})

        deploy_payload["tables"] = template["tables"]
        deploy_payload["lists"] = template["lists"]

        if payload_filename is not None and payload_directory is not None:
            mk_dir(payload_directory)
            save_json(
                os.path.join(payload_directory, payload_filename),
                deploy_payload
            )

        return deploy_payload

    def flatten_template(self, parent, child, template_dir):
        logging.info("processing parent file \"{}\"".format(parent))

        parent_dict = self.read_template(
            os.path.join(template_dir, parent))

        # Recursion happens here
        if 'parent' in parent_dict:
            parent_dict = self.flatten_template(
                os.path.join(template_dir, parent_dict["parent"]),
                parent_dict, template_dir)

        # Process the child objects 'strings' and 'tables' keys.
        child_strings = {}
        child_tables = {}
        logging.debug("[{}] starting merge".format(parent))
        if 'strings' in child:
            for string in child["strings"]:
                k, v = string.popitem()
                logging.debug("[{}] child: {}".format(parent, k))
                child_strings[k] = v

        if 'tables' in child:
            i = 0
            for table in child["tables"]:
                logging.debug("[{}] iapptable {}".format(parent, table["name"]))
                child_tables[table["name"]] = i
                i += 1

        # Merge with the parent dictionary giving precedence to the child's values
        if 'strings' in parent_dict:
            for string in parent_dict["strings"]:
                k, v = string.popitem()
                if k in child_strings.keys():
                    string[k] = child_strings[k]
                    logging.debug(
                        "[{}] OVERRIDE: {}: {}".format(parent, k, string[k]))
                else:
                    string[k] = v

        if 'tables' in parent_dict:
            i = 0
            for table in parent_dict["tables"]:
                if table["name"] in child_tables.keys():
                    logging.debug(
                        "[{}] OVERRIDE TABLE: {}".format(
                            parent, table["name"]))
                    parent_dict["tables"][i] = child["tables"][child_tables[table["name"]]]
                i += 1

        if 'lists' in parent_dict:
            i = 0
            for alist in parent_dict["lists"]:
                if alist["name"] in child_tables.keys():
                    logging.debug(
                        "[{}] OVERRIDE LIST: {}".format(parent, alist["name"]))
                    parent_dict["lists"][i] = child["lists"][child_tables[alist["name"]]]
                i += 1

        # Inherit any other top level keys
        for topitem in child.keys():
            logging.debug("top item={}".format(topitem))
            if topitem not in ["tables", "strings"]:
                parent_dict[topitem] = child[topitem]

        return parent_dict
