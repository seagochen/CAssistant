#!/bin/env python3
# -*- coding: utf-8 -*-
# Author: Orlando Chen
# Created: Jul 28, 2020
# Modified: Jul 28, 2020

import untangle
import pkgconfig


class PKGConfigs(object):

    def __init__(self, name):
        self.flags = None
        self.libs = None

        self.pkg_search_libs_only(name)
        self.pkg_search_headers_only(name)

    def pkg_search_headers_only(self, name):
        if pkgconfig.exists(name):
            self.flags = f"{pkgconfig.cflags(name)}"
        else:
            self.flags = None

    def pkg_search_libs_only(self, name):
        if pkgconfig.exists(name):
            self.flags = f"{pkgconfig.libs(name)}"
        else:
            self.flags = None

    def __str__(self):
        if self.flags is None and self.libs is not None:
            return self.libs

        if self.flags is not None and self.libs is None:
            return self.flags

        if self.flags is None and self.libs is None:
            return ""

        return f"{self.flags} {self.libs}"


class XMLDefinedCompiler(object):

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
            self.pkg_configs = []
            for token in xml.config.requirements.pkgs.item:

                # search and verify pkg config information
                config = PKGConfigs(token.cdata)
                self.pkg_configs.append(config)

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
