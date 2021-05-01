#!/bin/env python3
# -*- coding: utf-8 -*-

import pkgconfig


class PKGParser(object):

    def __init__(self, name):
        self.headers = None
        self.libs = None

        self.pkg_search_libs_only(name)
        self.pkg_search_headers_only(name)

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
