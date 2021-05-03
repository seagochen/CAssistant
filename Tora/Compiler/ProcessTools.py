#!/bin/env python3
# -*- coding: utf-8 -*-

from Tora.XmlParser.ProjectParser import ProjectParser
from Tora.XmlParser.SolutionParser import SolutionParser
from siki.basics import Exceptions


def project_headers(project: ProjectParser):
    if project["includes"] is not None:
        return "-I" + " -I".join(project["includes"])

    else:
        return None


def project_libraries(project: ProjectParser):
    libraries = []

    if project["libraries"] is not None:

        for key, val in project["libraries"].items():
            libraries.append(f"-L{key} {' '.join(val)}")

        return ' '.join(libraries)
    else:
        return None


def project_sources(project: ProjectParser):
    if project.src_files:
        return project.src_files

    else:
        raise Exceptions.NoAvailableResourcesFoundException("sources cannot be null")


def compiler_pkg_configs(solution: SolutionParser):

    if solution.compiler['pkg_configs'] is not None:
        return [str(i) for i in solution.compiler['pkg_configs']]

    else:
        return None


def compiler_name(solution: SolutionParser):
    if solution.compiler["compiler"]:
        return solution.compiler["compiler"]

    else:
        raise Exceptions.NoAvailableResourcesFoundException("compiler cannot be null")


def compiler_flags(solution: SolutionParser):
    if solution.compiler["flags"]:
        return " ".join(solution.compiler["flags"])

    else:
        return None


def compiler_macros(solution: SolutionParser):
    if solution.compiler["macros"]:
        return " ".join(solution.compiler["macros"])

    else:
        return None


def null_filters(data: list):
    data.remove(None)