#!/bin/env python3
# -*- coding: utf-8 -*-
# Author: Orlando Chen
# Created: Jul 28, 2020
# Modified: Feb 10, 2021

import os

from siki.basics import Exceptions

from Tora.Components import ObjectFilesMan
from Tora.Components.ToraDB import TORA_TEMP
from Tora.Components.ToraDB import ToraDatabase
from Tora.Solutions.XMLDefinedSolution import XMLDefinedSolution


def __gen_links_and_headers(solution, project):
    links_and_headers = []

    if solution.compiler['pkg_configs'] is not None:
        links_and_headers = [str(i) for i in solution.compiler['pkg_configs']]

    if project['includes'] is not None:
        links_and_headers.extend(project['includes'])

    if project['libraries'] is not None:
        links_and_headers.extend(project['libraries'])

    # 编译该项目所需要链接的头文件和库文件
    return " ".join(links_and_headers)


def __gen_compiler_tags(solution):
    # 编译器
    compiler_tags = [solution.compiler['compiler']]

    # 编译标准
    if solution.compiler['flags'] is not None:
        compiler_tags.extend(solution.compiler.flags)

    # 宏命令
    if solution.compiler['macros'] is not None:
        compiler_tags.extend(solution.compiler['macros'])

    return " ".join(compiler_tags)


def __load_src_files(project):
    if len(project.src_files) <= 0:
        return []

    else:
        return project.src_files


def compiling_sources(xml_file: str):
    """
    use compiler to compile source file to object file
    """

    # create tora database
    database = ToraDatabase()

    # load xml solutions
    solution = XMLDefinedSolution(xml_file)
    for project in solution:
        # 项目所需链接的头文件和库文件
        headers_links = __gen_links_and_headers(solution, project)

        # 准备编译选项
        compiler_tags = __gen_compiler_tags(solution)

        # 编译文件
        src_files = __load_src_files(project)
        if len(src_files) <= 0:  # 空文件夹，跳过
            raise Exceptions.EmptyCollectionElementException(f"{project['name']} has no source files, skipped")

        else:  # 有源文件，编译
            for src_file in __load_src_files(project):

                # 检查文件信息，如果文件已经更新或第一次发现，文件进行编译
                if database.update_file_info(project['name'], src_file):

                    # 生成编译命令
                    cmd = f"{compiler_tags} {headers_links} {src_file} -c -o " \
                          f"{ObjectFilesMan.generate_object_file(project['name'], src_file, TORA_TEMP)}"
                    
                    # print debug message
                    # print(cmd)
                    print("exec:", f"generating object file from {src_file}...")

                    # cmd exe
                    os.system(cmd)

                # 更新数据库
                database.save_and_close()
