#!/bin/env python3
# -*- coding: utf-8 -*-

from siki.basics import Exceptions
from siki.basics import FileUtils

from Tora.XmlParser import LibrariesLinker


class ProjectParser(object):

    def __parse_src(self, project):
        if project.get_attribute("src") is None:
            raise Exceptions.InvalidParamException("Project cannot be indicated to an unknown source path")
        else:
            src_dir = project["src"]
            if not FileUtils.isdir(src_dir):
                self.src_files = []
            else:
                self.src_files = FileUtils.search_files(src_dir,
                                                        r"\.(c|cpp|C|CPP|Cpp|cuda|CUDA|cu|CU|Cu)$")

    def __parse_project_name(self, project):
        if project.get_attribute("name") is not None:
            self.name = project["name"]
        else:
            raise Exceptions.InvalidParamException("Project should have a name")

    def __parse_project_output_dir(self, project):
        if project.get_attribute("output") is not None:
            self.output = project["output"]
        else:
            raise Exceptions.InvalidParamException("Project should have an output dir")

    def __parse_project_output_type(self, project):
        if project.get_attribute("type") is not None:
            self.type = project["type"]

    def __parse_header(self, project):
        if hasattr(project, "includes"):
            include = project.includes
            headers = []

            for path in include.path:
                path_str = path.cdata

                if isinstance(path_str, str) and FileUtils.isdir(path_str):
                    headers.append(path_str)

            self.includes = headers

    def __parse_lib(self, project):
        if hasattr(project, "libraries"):
            self.libraries = LibrariesLinker.link(project.libraries)

    def __init__(self, proj):
        self.type = "exe"
        self.name = "a.out"
        self.output = "build"

        # 構成ファイルからプロジェクト名を読み取ります
        self.__parse_project_name(proj)

        # 構成ファイルからビルドパスを読み取ります
        self.__parse_project_output_dir(proj)

        # 構成ファイルからファイルタイプを取得する
        self.__parse_project_output_type(proj)

        # ソースコードのファイルアドレスを取得する
        self.__parse_src(proj)

        # ヘッダーファイルを解析します
        self.__parse_header(proj)

        # parse libs
        self.__parse_lib(proj)

    def __getitem__(self, item):
        if hasattr(self, item):
            return self.__dict__[item]
        return None

    def __str__(self):
        strings = [f"Name: '{self.name}'\ntype: '{self.type}'\noutput dir: '{self.output}'",
                   f"with sources: {self.src_files}"]

        if hasattr(self, 'includes'):
            strings.append(f"with headers: {self.includes}")

        if hasattr(self, 'libraries'):
            strings.append(f"with libraries: {self.libraries}")

        return "\n".join(strings)
