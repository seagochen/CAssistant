#!/bin/env python3
# -*- coding: utf-8 -*-
# Author: Orlando Chen
# Created: Jul 28, 2020
# Modified: Jul 28, 2020

import untangle
from siki.basics import FileUtils, Exceptions


def link_header(includes: untangle.Element):
    headers_link = []

    for header_path in includes.path:
        the_path = header_path.cdata

        if isinstance(the_path, str) and FileUtils.isdir(the_path):
            headers_link.append(f"-I{the_path}")

    return headers_link


def link_libraries(libraries: untangle.Element):
    libraries_link = []

    for library_path in libraries:

        # 对传入的库文件地址进行检测，如果不是文件夹，放弃
        if library_path.get_attribute("path") is not None and not FileUtils.isdir(library_path["path"]):
            continue

        # 用户使用了默认的系统库，通常搜寻的默认地址是/usr/lib
        if library_path.get_attribute("path") is None:
            for item in library_path.item:
                libraries_link.append(f"-l{item.cdata}")
            continue

        # 自定义库地址，或者第三方地址
        if hasattr(library_path, "item"):  # 查找所有列在item里的内容
            libraries = []
            for item in library_path.item:
                libraries.append(f"-l{item.cdata}")

            # 生成最终命令
            libraries_link.append(f"-L{library_path['path']} {' '.join(libraries)}")
            continue

        else:  # 只给了一个库地址，但没有指定需要链接哪些库，因此链接全部的静态库文件
            libraries = []
            for item in FileUtils.search_files(library_path['path'], r"\.a$"):  # 类linux系统，默认静态文件是libXXX.a
                _, leaf = FileUtils.root_leaf(item)
                libraries.append(f"-l{leaf[3:-2]}")

            # 生成最终命令
            libraries_link.append(f"-L{library_path['path']} {' '.join(libraries)}")

    return libraries_link


def search_src_files(src_dir: str):
    if not FileUtils.isdir(src_dir):
        return []

    # Tora 只用于协助编译C/CPP/CUDA代码，其他代码现在暂时不考虑
    return FileUtils.search_files(src_dir, r"\.(c|cpp|C|CPP|Cpp|cuda|CUDA|cu|CU|Cu)$")


class XMLDefinedProject(object):

    def __init__(self, project: untangle.Element):
        self.type = "exe"
        self.name = "a.out"
        self.output = "build"

        if project.get_attribute("name") is not None:
            self.name = project["name"]

        if project.get_attribute("output") is not None:
            self.output = project["output"]

        if project.get_attribute("type") is not None:
            self.type = project["type"]

        if project.get_attribute("src") is None:
            raise Exceptions.InvalidParamException("Project cannot be indicated to an unknown source path")
        else:
            self.src_files = search_src_files(project["src"])

        # 链接头文件
        if hasattr(project, "includes"):
            self.includes = link_header(project.includes)

        # 链接库文件
        if hasattr(project, "libraries"):
            self.libraries = link_libraries(project.libraries)

    def __getitem__(self, item):
        if hasattr(self, item):
            return self.__dict__[item]
        return None
