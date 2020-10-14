#!/bin/env python3
# -*- coding: utf-8 -*-
# Author: Orlando Chen
# Created: Oct 7, 2020
# Modified: Oct 7, 2020

import untangle

from Tora.Solutions.BasicCompilerParser import BasicCompilerDefined
from Tora.Solutions.BasicProjectParser import BasicProjectDefined


def configuration_verification(file: str):
    # check compiler configuration
    compiler = BasicCompilerDefined(file)
    print(compiler)

    # parsing the xml configuration file
    config = untangle.parse(file).config

    # iterate every configuration of each project
    for project in config.solution.project:

        print("---------------------------------------------------------------------------------------------------")
        project = BasicProjectDefined(project)
        print(project)
