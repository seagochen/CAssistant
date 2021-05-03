#!/bin/env python3
# -*- coding: utf-8 -*-

import untangle
from Tora.XmlParser.PKGParser import PKGParser


class CompilerParser(object):

    def __init__(self, filename):
        xml = untangle.parse(filename)

        # 構成ファイルから指定されたコンパイラ情報を取得します
        self.__parser_compiler(xml)

        # 構成ファイルから指定されたコンパイラのフラグ情報を取得します
        self.__parser_flags(xml)

        # 他の構成情報があれば、その情報を読み取って解析します
        if hasattr(xml.config.requirements, "pkgs"):
            self.__parse_pkg(xml)

        # if macros defined, parse the xml clause
        if hasattr(xml.config.requirements, "macros"):
            self.__parse_macros(xml)

    def __getitem__(self, item):
        if hasattr(self, item):
            return self.__dict__[item]
        return None

    def __str__(self):
        output = [f"Compiler: {self.compiler}"]

        # converting pkg config to string
        pkg_configs = self.__getitem__('pkg_configs')
        if pkg_configs is not None:
            headers = []
            libs = []

            # separately add the headers and libraries to the
            # header-list and lib-list
            for config in pkg_configs:
                if config.headers is not None:
                    headers.append(config.headers)
                if config.libs is not None:
                    libs.append(config.libs)

            # plain the list and convert them to the string
            if len(headers) > 0:
                output.append(f"with headers: { ' '.join(headers) }")
            if len(libs) > 0:
                output.append(f"with libs: { ' '.join(libs) }")

        # converting flags to string
        ret = self.__getitem__('flags')
        if ret is not None:
            output.append(f"with flags: { ' '.join(ret)}")

        # converting macros to string
        ret = self.__getitem__('macros')
        if ret is not None:
            output.append(f"with macros: { ' '.join(ret)}")

        # finally
        return "\n".join(output)

    def __parser_compiler(self, xml):
        self.compiler = xml.config.requirements["uses"]

    def __parser_flags(self, xml):
        if hasattr(xml.config.requirements, "flags"):
            self.flags = []
            for token in xml.config.requirements.flags.item:
                flag = f"-{token.cdata}"
                self.flags.append(flag)

    def __parse_pkg(self, xml):
        pkg_configs = []

        for token in xml.config.requirements.pkgs.item:

            # 確認して解決する
            config = PKGParser(token.cdata)
            if config.is_valid():
                pkg_configs.append(config)

        # データを持っている、追加する
        if len(pkg_configs) > 0:
            self.pkg_configs = pkg_configs

    def __parse_macros(self, xml):
        self.macros = []

        for token in xml.config.requirements.macros.define:

            # if "value" in token._attributes:
            if token.get_attribute("value") is not None:
                macro = f"-D{token['name']}={token['value']}"
            else:
                macro = f"-D{token['name']}"

            self.macros.append(macro)