#!/bin/env python3
"""
This file is trying to compile the given source file to obj-file
"""

# import siki
from siki.basics import FileUtils
from siki.basics import Exceptions

# import standard modules
import os
import sys

# import Tora modules
from ConfigReader import ConfigReader
import ToraDB as toradb

TORA_TEMP = ".tora/temp"


def object_name(filename, path=TORA_TEMP):
    """
    change the extension of file to object file 
    """
    if not FileUtils.exists(path):
        FileUtils.mkdir(path)

    # trim the original root of file path
    root, leaf = FileUtils.root_leaf(filename)
    filename = leaf

    if ".cpp" in filename:  # CPP file
        obj = filename.replace(".cpp", ".o")
        return FileUtils.gen_file_path(path, obj)

    if ".CPP" in filename:  # CPP file
        obj = filename.replace(".CPP", ".o")
        return FileUtils.gen_file_path(path, obj)

    if ".Cpp" in filename:  # CPP file
        obj = filename.replace(".Cpp", ".o")
        return FileUtils.gen_file_path(path, obj)

    if ".c" in filename:  # C file
        obj = filename.replace(".c", ".o")
        return FileUtils.gen_file_path(path, obj)

    if ".C" in filename:  # C file
        obj = filename.replace(".C", ".o")
        return FileUtils.gen_file_path(path, obj)

    if ".cuda" in filename:  # CUDA file
        obj = filename.replace(".cuda", ".o")
        return FileUtils.gen_file_path(path, obj)

    if ".cu" in filename:  # CUDA file
        obj = filename.replace(".cu", ".o")
        return FileUtils.gen_file_path(path, obj)


def compiling_internal_files(reader, path=TORA_TEMP):
    """
    use compiler to compile source file to object file
    """
    source_files = reader.src_list()
    if len(source_files) <= 0:
        raise Exceptions.InvalidParamException("config file is invalid")

    # create tora db
    database = toradb.create_tora_db()
    if database is None:
        raise Exceptions.NoAvailableResourcesFoundException("create tora db failed")

    # update each file's md5
    for src in source_files:

        if not toradb.update_tora_hash(src, database):
            continue  # file no need to compile

        # generate gcc/g++/nvcc commands
        cmdline = [reader.compiler(),
                   reader.includes(),
                   reader.src_flags(),
                   reader.src_macros(),
                   reader.sys_libs(),
                   src,
                   "-c -o",
                   object_name(src)]

        # for debug
        cmd = " ".join(cmdline)
        print("exec:", cmd)
        os.system(cmd)

    # update tora database
    toradb.write_tora_db(database)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise Exceptions.InvalidParamException("params len is not correct")

    # executing
    reader = ConfigReader(sys.argv[1])
    compiling_internal_files(reader)
