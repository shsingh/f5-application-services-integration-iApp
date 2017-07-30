#!/usr/bin/env python

import errno
import json
import logging
import logging.config
import os
import shutil
import time
from glob import glob

import yaml


def mk_dir(dir_name):
    try:
        os.makedirs(dir_name)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise
        pass
    return os.path.abspath(dir_name)


def rm_dir(my_dir):
    try:
        shutil.rmtree(
            os.path.abspath(my_dir)
        )
    except OSError:
        pass


def get_timestamp():
    return int(time.time())


def setup_logging(logging_cfg_file="logging.yaml", input_logging_level='INFO'):
    mk_dir("logs")
    if os.path.exists(logging_cfg_file):
        with open(logging_cfg_file, 'rt') as logging_cfg:
            config = yaml.safe_load(logging_cfg.read())
            logging.config.dictConfig(config)
    else:
        logging_level = 'INFO'
        if input_logging_level in ['INFO', 'DEBUG', 'WARNING',
                                   'ERROR', 'CRITICAL']:
            logging_level = input_logging_level

        numeric_level = getattr(logging, logging_level)
        logging.basicConfig(level=numeric_level)


def save_json(filename, json_content):
    logger = logging.getLogger(__name__)
    logger.debug("Saving file: {}".format(filename))
    with open(filename, 'w+') as template:
        json.dump(json_content, template, indent=4, sort_keys=True)


def fix_indents(path):
    for filename in glob(path):
        with open(filename, 'r') as template:
            json_content = json.load(template)

        save_json(filename, json_content)



