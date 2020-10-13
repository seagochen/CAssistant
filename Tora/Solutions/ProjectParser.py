#!/bin/env python3
# -*- coding: utf-8 -*-
# Author: Orlando Chen
# Created: Jul 28, 2020
# Modified: Jul 28, 2020

import untangle
from siki.basics import FileUtils, Exceptions
from Tora.Solutions.BasicProjectParser import BasicXMLDefined


def convert_libraries_link_info(key, val):
    if val is not None and len(val) > 0:
        clause = "-L" + key + " -l" + " -l".join(val)
        return clause

    return None


class XMLDefinedProject(BasicXMLDefined):

    def __init__(self, project: untangle.Element):
        super().__init__(project)

        print("Hi there")

        if len(self.includes) > 0:
            self.includes = "-I".join(self.includes)

        if len(self.libraries) > 0:
            link_libs = []

            for key, val in self.libraries.items():
                clause = convert_libraries_link_info(key, val)
                if clause is not None:
                    link_libs.append(clause)

            # dict transforms to string clause
            self.libraries = " ".join(link_libs)
