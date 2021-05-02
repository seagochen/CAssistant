#!/bin/env python3
# -*- coding: utf-8 -*-

import untangle
import platform

from siki.basics import FileUtils
from siki.dstruct import DictExtern
from siki.basics import Exceptions


def search_custom_libs(library: untangle.Element):
    path = library.get_attribute("path")

    if FileUtils.isdir(path):
        if platform.system() == "Linux":
            return FileUtils.search_files(path, r"[\.a|\.so]$")

        elif platform.system() == "Darwin":
            return FileUtils.search_files(path, r"[\.dylib|\.so]$")

    else:
        raise Exceptions.InvalidParamException(f"not available path: {path} for "
                                               f"searching libraries")


def search_specified_libs(library: untangle.Element):
    defaults = []

    for item in library.item:
        defaults.append(item.cdata)

    return defaults


def link(libraries: untangle.Element):
    # library link
    library_link = {}

    for library in libraries:
        # third part library
        if library.get_attribute("path") is not None:

            key_name = library.get_attribute("path")

            if hasattr(library, 'item'):
                items = search_specified_libs(library)
                library_link = DictExtern.union(
                    library_link, {key_name: items})
            else:
                items = search_custom_libs(library)
                library_link = DictExtern.union(
                    library_link, {key_name: items})

        else:  # default
            items = search_specified_libs(library)
            library_link = DictExtern.union(library_link, {"default": items})

    return library_link
