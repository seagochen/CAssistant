#!/bin/env python3
# -*- coding: utf-8 -*-
# Author: Orlando Chen
# Created: Jul 28, 2020
# Modified: Feb 10, 2021

import untangle
from siki.basics import FileUtils, Exceptions
from Tora.Solutions.BasicProjectParser import BasicProjectDefined


def convert_libraries_link_info(key, val):
    if key == "default":
        return " ".join(val)

    if val is not None and len(val) > 0:
        return "-L" + key + " " + " ".join(val)

    return None


class XMLDefinedProject(BasicProjectDefined):

    def __init__(self, project: untangle.Element):
        super().__init__(project)

        if hasattr(self, 'includes') and len(self.includes) > 0:
            includes = []
            for inc in self.includes:
                includes.append(f"-I{inc}")
            self.includes = includes

        if hasattr(self, 'libraries') and len(self.libraries) > 0:
            link_libs = []

            for key, val in self.libraries.items():
                clause = convert_libraries_link_info(key, val)
                if clause is not None:
                    link_libs.append(clause)

            # dict transforms to string clause
            self.libraries = link_libs
