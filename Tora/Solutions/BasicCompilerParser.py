#!/bin/env python3
# -*- coding: utf-8 -*-
# Author: Orlando Chen
# Created: Oct 14, 2020
# Modified: Oct 14, 2020

import untangle
import pkgconfig
from Tora import Utilities


class PKGConfigs(object):

    def __init__(self, name):
        self.headers = None
        self.libs = None

        self.pkg_search_libs_only(name)
        self.pkg_search_headers_only(name)

        # print(self.headers)
        # print(self.libs)

    def pkg_search_headers_only(self, name):
        if pkgconfig.exists(name):
            self.headers = f"{pkgconfig.cflags(name)}"
        else:
            self.headers = None

    def pkg_search_libs_only(self, name):
        if pkgconfig.exists(name):
            self.libs = f"{pkgconfig.libs(name)}"
        else:
            self.libs = None

    def __str__(self):
        if self.headers is None and self.libs is not None:
            return self.libs

        if self.headers is not None and self.libs is None:
            return self.headers

        if self.headers is None and self.libs is None:
            return ""

        return f"{self.headers} {self.libs}"

    def is_valid(self):
        if self.headers is None and self.libs is None:
            return False
        else:
            return True


class BasicCompilerDefined(object):

    def __init__(self, filename):
        xml = untangle.parse(filename)

        # get the compiler name
        self.compiler = xml.config.requirements["uses"]

        # get the flags
        if hasattr(xml.config.requirements, "flags"):
            self.flags = []
            for token in xml.config.requirements.flags.item:
                flag = f"-{token.cdata}"
                self.flags.append(flag)

        # append pkg-configs if it has
        if hasattr(xml.config.requirements, "pkgs"):
            pkg_configs = []
            for token in xml.config.requirements.pkgs.item:

                # search and verify pkg config information
                config = PKGConfigs(token.cdata)
                if config.is_valid():
                    pkg_configs.append(config)

            if len(pkg_configs) > 0:  # assign valid array only
                self.pkg_configs = pkg_configs

        # append defined macros it it has
        if hasattr(xml.config.requirements, "macros"):
            self.macros = []
            for token in xml.config.requirements.macros.define:

                # if "value" in token._attributes:
                if token.get_attribute("value") is not None:
                    macro = f"-D{token['name']}={token['value']}"
                else:
                    macro = f"-D{token['name']}"

                self.macros.append(macro)

    def __getitem__(self, item):
        if hasattr(self, item):
            return self.__dict__[item]
        return None

    def __str__(self):
        strings = [f"Compiler: {self.compiler}"]

        ret = self.__getitem__('pkg_configs')
        if ret is not None:
            headers = []
            libs = []

            for pkg in ret:
                Utilities.discard_nil(pkg.headers, headers.append)
                Utilities.discard_nil(pkg.libs, libs.append)

            # plain the list
            if len(headers) > 0:
                strings.append(f"with headers: { ' '.join(headers) }")
            if len(libs) > 0:
                strings.append(f"with libs: { ' '.join(libs) }")

        ret = self.__getitem__('flags')
        if ret is not None:
            strings.append(f"with flags: { ' '.join(ret)}")

        ret = self.__getitem__('macros')
        if ret is not None:
            strings.append(f"with macros: { ' '.join(ret)}")

        return "\n".join(strings)
