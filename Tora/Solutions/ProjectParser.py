#!/bin/env python3
# -*- coding: utf-8 -*-
# Author: Orlando Chen
# Created: Jul 28, 2020
# Modified: Jul 28, 2020

import untangle
from siki.basics import FileUtils, Exceptions
from Tora.Solutions.BasicProjectParser import BasicProjectDefined


def convert_libraries_link_info(key, val):
    if val is not None and len(val) > 0:
        clause = "-L" + key + " -l" + " -l".join(val)
        return clause

    return None


class XMLDefinedProject(BasicProjectDefined):

    def __init__(self, project: untangle.Element):
        super().__init__(project)

        if len(self.includes) > 0:
            includes = []
            for inc in self.includes:
                includes.append(f"-I{inc}")
            self.includes = includes

        if len(self.libraries) > 0:
            link_libs = []

            for key, val in self.libraries.items():
                clause = convert_libraries_link_info(key, val)
                if clause is not None:
                    link_libs.append(clause)

            # dict transforms to string clause
            self.libraries = link_libs
