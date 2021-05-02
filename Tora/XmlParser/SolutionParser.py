#!/bin/env python3
# -*- coding: utf-8 -*-

import untangle

from Tora.XmlParser.CompilerParser import CompilerParser
from Tora.XmlParser.ProjectParser import ProjectParser


class SolutionParser(object):

    def __init__(self, filename: str):
        """
        从配置文件中，获得关于编译器的配置信息和项目的配置信息
        """
        xml_reader = untangle.parse(filename)

        projects = []
        for project in xml_reader.config.solution.project:
            xml_project = ProjectParser(project)
            projects.append(xml_project)

        compiler = CompilerParser(filename)

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

    def __len__(self):
        return len(self.projects)

    def __str__(self):
        compiler_str = f"compiler: {str(self.compiler)}\n---------------------"
        project_str = ""

        for proj in self.projects:
            project_str += f"{str(proj)}\n---------------------\n"

        return f"{compiler_str}\n{project_str}"


