#!/bin/env python3
# -*- coding: utf-8 -*-
# Author: Orlando Chen
# Created: Oct 7, 2020
# Modified: Oct 7, 2020

import untangle

from Tora.Solutions.BasicProjectParser import BasicXMLDefined
from siki.basics import Exceptions


def configuration_verification(file: str):
    # parsing the xml configuration file
    config = untangle.parse(file).config

    # iterate every configuration of each project
    for project in config.solution.project:
        defined_project = BasicXMLDefined(project)

        print(f"Project name: [{ defined_project['name'] }]")

        # print out source files
        print("Source files:", defined_project.src_files)

        # print out header files
        print("Header files:", defined_project.includes)

        # print out libs
        print("Libraries:", defined_project.libraries)

    # iterate the configuration of every project
    return False, "hello world"
