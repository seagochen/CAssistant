#!/bin/env python3
# -*- coding: utf-8 -*-

import untangle
import os

from siki.basics import FileUtils
from siki.dstruct import DictExtern


def preprocess_libraries(lib: str):
    root, leaf = FileUtils.root_leaf(lib)

    if os.name == "Linux":
        if leaf[0:3] == "lib":
            if leaf[-3:] == ".so":
                return f"-l{leaf[3:-3]}"
            if leaf[-2:] == ".a":
                return f"-l{leaf[3:-2]}"
    elif os.name == "Darwin":
        if leaf[0:3] == "lib":
            if leaf[-6:] == ".dylib":
                return f"-l{leaf[3:-6]}"
            if leaf[-3:] == ".so":
                return f"-l{leaf[3:-3]}"
    return lib


def link_custom_libs(library_path: untangle.Element):
    """
    link system default libraries
    """
    custom_lib = {}

    # customized library or third-party library
    if hasattr(library_path, "item"):  # with specified the files
        libraries = []
        for item in library_path.item:
            libraries.append(item.cdata)

        # finally
        custom_lib[library_path['path']] = libraries

    else:  # with only a path, search and links all libraries as possible
        libraries = []

        for lib in FileUtils.search_files(library_path['path'], r"[\.a|\.so]$"):
            libraries.append(preprocess_libraries(lib))

        # finally
        custom_lib[library_path['path']] = libraries

    return custom_lib


def link(libraries: untangle.Element):
    libraries_link = {}

    for library_path in libraries:

        # 对传入的库文件地址进行检测，如果不是文件夹，放弃
        if library_path.get_attribute("path") is not None and not FileUtils.isdir(library_path["path"]):

            # 如果给定的地址时相对地址，那么重新生成绝对地址后，再次尝试
            new_path = FileUtils.gen_folder_path(FileUtils.pwd(), library_path["path"])
            if FileUtils.isdir(new_path):
                library_path["path"] = new_path

            # 解析失败，放弃
            else:
                continue

        # 用户使用了默认的系统库，通常搜寻的默认地址是/usr/lib
        if library_path.get_attribute("path") is None:
            libraries = []

            for item in library_path.item:
                libraries.append(item.cdata)

            # 如果之前已经解析，那么就对数据进行增量操作
            if "default" in libraries_link.keys():
                libraries_link = DictExtern.union(libraries_link, {"default": libraries})
            else:
                libraries_link["default"] = libraries

            # 解析结束，进入下一步
            continue

        # 自定义库地址，或者第三方地址
        custom_libs = link_custom_libs(library_path)
        if len(custom_libs) > 0:
            libraries_link = DictExtern.union(libraries_link, custom_libs)

    return libraries_link
