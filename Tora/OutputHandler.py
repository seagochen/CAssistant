#!/bin/env python3
# -*- coding: utf-8 -*-
# Author: Orlando Chen
# Created: Jul 28, 2020
# Modified: Jul 28, 2020

from Tora.Components.ToraDB import TORA_TEMP
from Tora.Solutions.XMLDefinedSolution import XMLDefinedSolution

import os
from siki.basics import FileUtils
from siki.basics import Exceptions


def __search_object_files(project_name: str, temp_path=TORA_TEMP):
    folder_path = FileUtils.gen_folder_path(temp_path, project_name)

    # 检查文件夹地址是否存在
    if not FileUtils.exists(folder_path):
        raise Exceptions.NoAvailableResourcesFoundException(f"Cannot found folder: {folder_path}")

    # 从文件夹里检索.o文件
    obj_files = FileUtils.search_files(folder_path, "\w+\.o$")

    # 返回检索结果
    return obj_files


def __gen_links(solution, project):
    links = []

    if solution.compiler['pkg_configs'] is not None:
        links = [i.libs for i in solution.compiler['pkg_configs']]

    if project['libraries'] is not None:
        links.extend(project['libraries'])

    # 编译该项目所需要链接的头文件和库文件
    return " ".join(links)


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


def __gen_executive_file(solution, project):

    # obj files
    obj_files = __search_object_files(project['name'])
    obj_files = " ".join(obj_files)

    # 生成文件的地址
    final_path = FileUtils.gen_file_path(project['output'], project['name'])

    # 如果目标文件夹没有生成
    if not FileUtils.exists(project['output']):
        FileUtils.mkdir(project['output'])

    # 编译命令
    cmd = f"{__gen_compiler_tags(solution)} {obj_files} {__gen_links(solution, project)} -o {final_path}"

    # 执行命令
    print("exec:", f"generating executive file to {project['output']}...")
    os.system(cmd)


def __gen_static_file(project):

    # obj files
    obj_files = __search_object_files(project['name'])
    obj_files = " ".join(obj_files)

    # 生成文件的地址
    final_path = FileUtils.gen_file_path(project['output'], f"lib{project['name']}.a")

    # 如果目标文件夹没有生成
    if not FileUtils.exists(project['output']):
        FileUtils.mkdir(project['output'])

    # 编译命令
    cmd = f"ar -rcs {final_path} {obj_files}"

    # 执行命令
    print("exec:", f"generating static file to {project['output']}...")
    os.system(cmd)


def __gen_shared_file(solution, project):
    # obj files
    obj_files = __search_object_files(project['name'])
    obj_files = " ".join(obj_files)

    # 生成文件的地址
    final_path = FileUtils.gen_file_path(project['output'], f"lib{project['name']}.so")

    # 如果目标文件夹没有生成
    if not FileUtils.exists(project['output']):
        FileUtils.mkdir(project['output'])

    # 编译命令
    cmd = f"{__gen_compiler_tags(solution)} -shared -fPIC {__gen_links(solution, project)} {obj_files} -o {final_path}"

    # 执行命令
    print("exec:", f"generating shared file to {project['output']}...")
    os.system(cmd)

    # 生成动态文件
    __gen_static_file(project)


def generate_final(xml_file: str):

    # 解析xml文件
    solution = XMLDefinedSolution(xml_file)

    # 对每个独立的项目进行单独编译
    for project in solution.projects:

        if project['type'] == 'dynamic':  # 生成动态文件
            __gen_shared_file(solution, project)
            continue

        if project['type'] == 'static':  # 只生成静态文件
            __gen_static_file(project)
            continue

        if project['type'] == 'exe':  # 生成执行文件
            __gen_executive_file(solution, project)
            continue
