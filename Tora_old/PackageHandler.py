#!/bin/env python3
# -*- coding: utf-8 -*-
# Author: Orlando Chen
# Created: Jul 28, 2020
# Modified: Oct 07, 2020

import untangle
import os
from siki.basics import FileUtils


def __file_full_root(file_path: str):
    _, leaf = FileUtils.root_leaf(file_path)
    return file_path.replace(leaf, "")


def __copy_incs(path_from, path_to):

    if not FileUtils.exists(path_to):
        FileUtils.mkdir(path_to)

    # 从给定的文件地址中搜索头文件
    headers = FileUtils.search_files(path_from, r"\.(h|H|hpp|HPP|Hpp)$")

    # 遍历文件，并创建新的文件地址
    for header in headers:

        # 把文件给定地址进行省略掉
        leaf_name = header.replace(path_from, "")
        leaf_name = leaf_name[1:]

        # 新文件名
        new_file = FileUtils.gen_file_path(path_to, leaf_name)
        new_sub_dir = __file_full_root(new_file)

        # 创建子文件夹
        if not FileUtils.exists(new_sub_dir):
            FileUtils.mkdir(new_sub_dir)

        # 拷贝文件内容
        FileUtils.copy(header, new_file)


def __copy_data(path_from, path_to):

    if not FileUtils.exists(path_to):
        FileUtils.mkdir(path_to)

    # 直接调用系统命令，把文件拷贝到给定地址
    os.system(f"cp -r {path_from} {path_to}")


def __copy_file(path_from, path_to):

    if not FileUtils.exists(path_to):
        FileUtils.mkdir(path_to)

    # 新的文件名
    _, leaf = FileUtils.root_leaf(path_from)
    new_file = FileUtils.gen_file_path(path_to, leaf)

    # 拷贝
    FileUtils.copy(path_from, new_file)


def generate_package(xml_file: str):
    """
    从配置文件中，获得关于打包信息
    """
    xml_reader = untangle.parse(xml_file)

    # 拷贝数据
    if hasattr(xml_reader.package, "data"):
        for path in xml_reader.package.data.dir:
            __copy_data(path['path'], path['to'])

    # 拷贝头文件
    if hasattr(xml_reader.package, "incs"):
        for path in xml_reader.package.incs.dir:
            __copy_incs(path['path'], path['to'])

    # 拷贝其他文件
    if hasattr(xml_reader.package, "files"):
        for path in xml_reader.package.files.file:
            __copy_file(path['path'], path['to'])
