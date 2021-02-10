#!/bin/env python3
# -*- coding: utf-8 -*-
# Author: Orlando Chen
# Created: Oct 7, 2020
# Modified: Oct 7, 2020

import untangle
from siki.basics import FileUtils
from Tora.Solutions.XMLDefinedSolution import XMLDefinedSolution


def check_project_configuration(project, errors: list):

    if hasattr(project, "includes"):

        # the include directories check
        for path in project.includes:
            if not FileUtils.exists(path[2:]):  # path not exists, check failed!
                errors.append(f"The include path {path[2:]} not valid for the project {project['name']}")

        # the libraries directories check
        print(project.libraries)


def configuration_verification(file: str):

    # parsing the xml configuration file
    xml = untangle.parse(file)

    # feedback message
    feedback = []

    solution = XMLDefinedSolution(file)
    for proj in solution.projects:
        print(proj.libraries)

    # iterate the configuration of every project
    return False, "hello world"
