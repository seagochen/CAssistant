#!/bin/env python3
# -*- coding: utf-8 -*-
# Author: Orlando Chen
# Created: Jul 30, 2020
# Modified: Jul 30, 2020

from Tora import PackageHandler
from Tora import SourceHandler
from Tora import OutputHandler

import os
import sys
import wget

from siki.basics import FileUtils


def help_msg():
    print("""
    tora compile <xml>      To compile the solution according to the given xml rules
    tora package <xml>      To package the solution according to the given xml rules
    tora prepare <dir>      To generate a blank solution under the current directory
    tora update             Update the Tora by using pip3
    tora help               To display available messages
    """)


def update_tora():
    print("Now, tora is trying to update itself by using pip3...")
    cmd = "pip3 install --upgrade tora"
    os.system(cmd)
    print("Done...")


def prepare_solution(folder="MySolution"):
    # 创建文件夹
    FileUtils.mkdir(folder)
    print(f"The {folder} has created by the script.",
          "Now it tries to download the configuration files from the GitHub...")

    # 配置文件地址拼接
    compile_url = "https://raw.githubusercontent.com/seagochen/tora/master/Resources/solution.xml"
    package_url = "https://raw.githubusercontent.com/seagochen/tora/master/Resources/package.xml"

    # 下载文件
    wget.download(compile_url, f"{folder}/solution.xml")
    wget.download(package_url, f"{folder}/package.xml")

    print("Done...")


def package_solution(xml="package.xml"):
    PackageHandler.generate_package(xml)
    print("Done...")


def compile_solution(xml="solution.xml"):
    SourceHandler.compiling_sources(xml)
    OutputHandler.generate_final(xml)


if __name__ == "__main__":

    # 用户没有指定, 或者指令为help
    if len(sys.argv) <= 1 or sys.argv[1] == 'help':
        help_msg()

    # 用户指令为update, 尝试更新tora
    if sys.argv[1] == 'update':
        update_tora()

    # 用户指令为prepare，创建空白的工程项目
    if sys.argv[1] == 'prepare':
        if len(sys.argv) == 3:
            prepare_solution(sys.argv[2])
        else:
            prepare_solution()

    # 用户指令为package, 对工程进行打包
    if sys.argv[1] == 'package':
        if len(sys.argv) == 3:
            package_solution(sys.argv[2])
        else:
            package_solution()






