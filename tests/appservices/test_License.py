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

import fnmatch
import os
from itertools import islice
import logging


def get_license_text():
    return """#!/usr/bin/env python
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
#     limitations under the License.""".split("\n")


def test_license(setup_logging):
    logger = logging.getLogger(__name__)
    matches = []

    for root, _, filenames in os.walk('./'):
        for filename in fnmatch.filter(filenames, '*.py'):
            matches.append(os.path.join(root, filename))

    for filename in matches:
        correct_header = get_license_text()

        with open(filename) as python_file:
            head = list(islice(
                python_file, len(correct_header)))

        file_license = []
        for line in head:
            file_license.append(line.strip())

        try:
            assert file_license == correct_header
        except AssertionError as ex:
            logger.error("File {} failed the test".format(filename))
            logger.exception(ex)
            raise
