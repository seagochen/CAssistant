#!/bin/env python3
# -*- coding: utf-8 -*-
# Author: Orlando Chen
# Created: Jul 28, 2020
# Modified: Jul 28, 2020

import untangle

from Tora.Solutions.CompilerParser import XMLDefinedCompiler
from Tora.Solutions.ProjectParser import XMLDefinedProject


class XMLDefinedSolution(object):

    def __init__(self, filename: str):
        """
        从配置文件中，获得关于编译器的配置信息和项目的配置信息
        """
        xml_reader = untangle.parse(filename)

        projects = []
        for project in xml_reader.config.solution.project:
            xml_project = XMLDefinedProject(project)
            projects.append(xml_project)

        compiler = XMLDefinedCompiler(filename)

        self.compiler = compiler
        self.projects = projects

    def __next__(self):
        if self.anchor < len(self.projects):
            try:
                return self.projects[self.anchor]
            finally:
                self.anchor += 1
        else:
            raise StopIteration

    def __iter__(self):
        self.anchor = 0
        return self
