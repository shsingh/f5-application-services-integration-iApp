#!/usr/bin/env python

import argparse
import os
import sys
import shutil
from src.appservices.Builder import AppServicesBuilder
from src.appservices.tools import mk_dir
from src.appservices.tools import rm_dir


def cli_parser():
    parser = argparse.ArgumentParser(
        description='Management script for the App Service'
                    ' Integration iApp template')
    parser.add_argument("-a", "--append",
                        default="",
                        help="A string to append to the base template name")
    parser.add_argument("-b", "--bundledir",
                        default="bundled",
                        help="The directory to use for bundled resources")
    parser.add_argument("-d", "--docs",
                        default=False,
                        action="store_true",
                        help="Build the documentation")
    parser.add_argument("-o", "--outfile",
                        help="The name of the output file")
    parser.add_argument("-p", "--preso",
                        default="presentation_layer.json",
                        help="The presentation layer JSON schema")
    parser.add_argument("-r", "--master_template",
                        default="master.template",
                        help="The root template file to use"
                             " (default: <basedir>/src/master.template")
    parser.add_argument("-w", "--build_dir",
                        default='build',
                        help="The root directory of source tree")
    parser.add_argument("-c", "--clean",
                        action="store_true",
                        help="Clean build")

    return parser


def router(parser, argv):
    args = parser.parse_args()
    if len(argv) < 1:
        parser.print_help()
        sys.exit(1)

    if args.clean:
        clean()

    if args.build_dir:
        clean()
        build_iapp(args.build_dir, args.bundledir, args.master_template)

    if args.docs:
        build_documentation()


def clean():
    rm_dir('build')


def build_documentation():
    os.system("cd docs && make clean && make html && cd ..")


def build_iapp(build_dir, bundle_dir, master_template):

    build_dir = mk_dir(build_dir)
    tmp_dir = mk_dir('tmp')
    resource_dir = os.path.abspath(os.path.join('src', 'resources'))

    builder = AppServicesBuilder(
        build_dir=build_dir,
        resource_dir=resource_dir,
        tempdir=tmp_dir,
        bundledir=bundle_dir,
        roottmpl=master_template
    )

    builder.buildAPL()
    builder.buildTemplate(
        build_dir=build_dir,
        resource_dir=resource_dir,
        tempdir=tmp_dir,
        bundledir=bundle_dir,
        roottmpl=master_template)

    builder.buildiWfTemplate()

    print("Assembling TCL only template...")
    outfile = os.path.join(build_dir, 'iapp.tcl')
    roottmpl = os.path.join(resource_dir, 'implementation_only.template')
    builder.buildTemplate(outfile=outfile, roottmpl=roottmpl)

    print("Assembling APL only template...")
    outfile = os.path.join(build_dir, 'iapp.apl')
    roottmpl = os.path.join(tmp_dir, 'apl.build')
    builder.buildTemplate(outfile=outfile, roottmpl=roottmpl)

    print("Assembling CLI script only template...")
    outfile = os.path.join(build_dir, 'appsvcs.integration.util.tcl')
    roottmpl = os.path.join(resource_dir, 'outside_util.tcl')
    builder.buildTemplate(outfile=outfile, roottmpl=roottmpl)

    print("Generating BIGIP JSON template...")
    builder.buildJsonTemplate()

    print("Generating Postman Collection...")
    outfile = os.path.join(
        build_dir,
        'AppSvcs_iApp_Workflows.postman_collection.json')
    roottmpl = os.path.join(
        resource_dir,
        'AppSvcs_iApp_Workflows.postman_collection.template')
    builder.buildTemplate(outfile=outfile, roottmpl=roottmpl)

    shutil.rmtree(tmp_dir)

if __name__ == '__main__':
    router(cli_parser(), sys.argv)
