#!/bin/env python3
# -*- coding: utf-8 -*-

from Tora.XmlParser.ProjectParser import ProjectParser
from Tora.XmlParser.SolutionParser import SolutionParser
from Tora.Components.ToraDatabase import TORA_TEMP
from siki.basics import Exceptions
from siki.basics import FileUtils

import platform


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
        raise Exceptions.NoAvailableResourcesFoundException(
            "sources cannot be null")


def compiler_pkg_configs(solution: SolutionParser):

    if solution.compiler['pkg_configs'] is not None:
        return [str(i) for i in solution.compiler['pkg_configs']]

    else:
        return None


def compiler_name(solution: SolutionParser):
    if solution.compiler["compiler"]:
        return solution.compiler["compiler"]

    else:
        raise Exceptions.NoAvailableResourcesFoundException(
            "compiler cannot be null")


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


def search_object_files(project: ProjectParser, temp=TORA_TEMP):
    folder_path = FileUtils.gen_folder_path(temp, project["name"])

    # if folder not exists
    if not FileUtils.exists(folder_path):
        raise Exceptions.NoAvailableResourcesFoundException(
            f"cannot found folder{folder_path}")

    # search object files from the given folder
    return FileUtils.search_files(folder_path, r"\w+\.o$")


def generate_static_file(solution: SolutionParser, project: ProjectParser):
    compiler = compiler_name(solution)
    libraries = project_libraries(project)

    objects = search_object_files(project)
    objects = " ".join(objects)

    # if the output path not exits
    if not FileUtils.exists(project["output"]):
        FileUtils.mkdir(project["output"])

    # generate command under different system
    if platform.system() == "Darwin":
        final_path = FileUtils.gen_file_path(project['output'],
                                             f"lib{project['name']}.dylib")
        return [compiler, objects, libraries, "-dynamiclib -o", final_path]

    elif platform.system() == "Linux":
        final_path = FileUtils.gen_file_path(project['output'],
                                             f"lib{project['name']}.a")
        return ["ar", objects, libraries, "-rcs", final_path]

    else:
        raise Exceptions.NoAvailableResourcesFoundException(
            "Null implementation under windows platform")


def generate_dynamic_file(solution: SolutionParser, project: ProjectParser):
    libraries = project_libraries(project)

    objects = search_object_files(project)
    objects = " ".join(objects)

    compiler = compiler_name(solution)
    pkg = compiler_pkg_configs(solution)
    flags = compiler_flags(solution)
    macros = compiler_macros(solution)

    # 生成文件的地址
    final_path = FileUtils.gen_file_path(project['output'],
                                         f"lib{project['name']}.so")

    # if the output path not exits
    if not FileUtils.exists(project["output"]):
        FileUtils.mkdir(project["output"])

    # finally
    return [compiler, pkg, flags, macros, libraries, objects, "-shared -fPIC", final_path]


def generate_executive_file(solution: SolutionParser, project: ProjectParser):
    libraries = project_libraries(project)
    objects = search_object_files(project)
    objects = " ".join(objects)

    compiler = compiler_name(solution)
    pkg = compiler_pkg_configs(solution)
    flags = compiler_flags(solution)
    macros = compiler_macros(solution)

    # 生成文件的地址
    final_path = FileUtils.gen_file_path(project['output'],
                                         f"lib{project['name']}.so")

    # if the output path not exits
    if not FileUtils.exists(project["output"]):
        FileUtils.mkdir(project["output"])

    # finally
    return [compiler, pkg, flags, macros, libraries, objects, "-o", final_path]
