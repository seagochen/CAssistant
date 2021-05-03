#!/bin/env python3
# -*- coding: utf-8 -*-


from Tora.Compiler import ProcessTools as tools
from Tora.XmlParser.SolutionParser import SolutionParser
from Tora.Components.ToraDatabase import ToraDatabase
from Tora.Components.ObjectFile import generate

from Tora.Components.ToraDatabase import TORA_TEMP

import os


class GCC(object):

    def __init__(self, xml: str):
        self.solution = SolutionParser(xml)
        self.database = ToraDatabase()

    def gen_objects(self):
        compiler = tools.compiler_name(self.solution)
        pkg = tools.compiler_pkg_configs(self.solution)
        flags = tools.compiler_flags(self.solution)
        macros = tools.compiler_macros(self.solution)

        for project in self.solution:
            headers = tools.project_headers(project)
            libraries = tools.project_libraries(project)
            sources = tools.project_sources(project)

            for src in sources:

                # 检查文件信息，如果文件已经更新或第一次发现，文件进行编译
                if self.database.update_file_info(project['name'], src):
                    # 生成编译命令
                    cmd = [compiler, pkg, flags, macros, headers, libraries,
                           src, " -c -o", generate(project['name'],
                                                   src, TORA_TEMP)]

                    # clean up None values
                    while None in cmd:
                        cmd.remove(None)

                    # print debug message
                    cmd = " ".join(cmd)
                    print(f"exec: {cmd}")

                    # run compiling command
                    os.system(cmd)

                # update database
                self.database.save_and_close()