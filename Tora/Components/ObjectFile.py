#!/bin/env python3
# -*- coding: utf-8 -*-

from siki.basics import FileUtils


def generate(project_name: str, filename: str, output_dir=None):
    """
    将源码文件转换为临时文件
    """

    # obj 文件存放地址
    if output_dir is not None:
        output_dir = FileUtils.gen_folder_path(output_dir, project_name)
    else:
        output_dir = project_name

    # 创建存放目录
    if not FileUtils.isdir(output_dir):
        FileUtils.mkdir(output_dir)

    # 对源文件地址进行分割, 并舍弃其根地址
    _, leaf = FileUtils.root_leaf(filename)
    filename = leaf

    # 生成临时文件地址
    if ".cpp" in filename:  # CPP file
        obj = filename.replace(".cpp", ".o")
        return FileUtils.gen_file_path(output_dir, obj)

    if ".CPP" in filename:  # CPP file
        obj = filename.replace(".CPP", ".o")
        return FileUtils.gen_file_path(output_dir, obj)

    if ".Cpp" in filename:  # CPP file
        obj = filename.replace(".Cpp", ".o")
        return FileUtils.gen_file_path(output_dir, obj)

    if ".c" in filename:  # C file
        obj = filename.replace(".c", ".o")
        return FileUtils.gen_file_path(output_dir, obj)

    if ".C" in filename:  # C file
        obj = filename.replace(".C", ".o")
        return FileUtils.gen_file_path(output_dir, obj)

    if ".cuda" in filename:  # CUDA file
        obj = filename.replace(".cuda", ".o")
        return FileUtils.gen_file_path(output_dir, obj)

    if ".cu" in filename:  # CUDA file
        obj = filename.replace(".cu", ".o")
        return FileUtils.gen_file_path(output_dir, obj)
