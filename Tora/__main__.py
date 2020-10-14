#!/bin/env python3
# -*- coding: utf-8 -*-
# Author: Orlando Chen
# Created: Jul 30, 2020
# Modified: Jul 30, 2020

import os
import sys

import wget
from siki.basics import FileUtils

from Tora import PackageHandler
from Tora import SourceHandler, OutputHandler, ProjectChecker


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


def clean_tora():
    print("Now, tora is trying to clean the buffers...")
    cmd = "rm -r .tora"
    os.system("rm -r .tora")


def prepare_solution(folder="MySolution"):
    # 创建文件夹
    FileUtils.mkdir(f"{folder}/src")
    print(f"The {folder} has created by the script.",
          "Now it tries to download the configuration files from the GitHub...")

    # 配置文件地址拼接
    compile_url = "https://raw.githubusercontent.com/seagochen/tora/master/Resources/solution.xml"
    package_url = "https://raw.githubusercontent.com/seagochen/tora/master/Resources/package.xml"

    # 下载文件
    print("Downloading solution file from remote server...")
    wget.download(compile_url, f"{folder}/solution.xml")
    print("Downloading package file from remote server...")
    wget.download(package_url, f"{folder}/package.xml")
    print("Downloading script file from remote server...")
    wget.download(package_url, f"{folder}/tora")

    # message feedback
    print("Done...")


def package_solution(xml="package.xml"):
    PackageHandler.generate_package(xml)


def compile_solution(xml="solution.xml"):
    ProjectChecker.configuration_verification(xml)
    SourceHandler.compiling_sources(xml)
    OutputHandler.generate_final(xml)
    print("Done")


class Switch(object):

    def __init__(self, value):
        self.value = value
        self.fall = False

    def __iter__(self):
        """Return the match method once, then stop"""
        yield self.match
        raise StopIteration

    def match(self, *args):
        """Indicate whether or not to enter a case suite"""
        if self.fall or not args:
            return True
        elif self.value in args:
            self.fall = True
            return True
        else:
            return False


if __name__ == "__main__":

    # 用户没有指定
    if len(sys.argv) <= 1:
        help_msg()
        exit(0)

    for case in Switch(sys.argv[1]):
        if case('help'):  # 指令为help
            help_msg()
            break

        if case('update'):  # 用户指令为update, 尝试更新tora
            update_tora()
            break

        if case('prepare'):  # 用户指令为prepare，创建空白的工程项目
            if len(sys.argv) == 3:
                prepare_solution(sys.argv[2])
            else:
                prepare_solution()
            break

        if case('compile'):  # 用户指令为compile, 编译工程项目
            if len(sys.argv) == 3:
                compile_solution(sys.argv[2])
            else:
                compile_solution()
            break

        if case('package'):  # 用户指令为package, 对工程进行打包
            if len(sys.argv) == 3:
                package_solution(sys.argv[2])
            else:
                package_solution()
            break

        if case('clean'):  # cleanup the temporary files
            clean_tora()
            break
