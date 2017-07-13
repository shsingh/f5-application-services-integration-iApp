#!/usr/bin/env python
import json
import glob

for filename in glob.glob("*.tmpl"):
    json_content = ''
    with open(filename, 'r') as template:
        json_content = json.load(template)

    with open(filename, 'w+') as template:
        json.dump(json_content, template, indent=4, sort_keys=True)
