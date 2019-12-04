#!/bin/env python3
"""
This file is trying to compile the given source file to obj-file
"""

# import siki
from siki.basics import FileUtils as fu
from siki.basics import Exceptions as excepts

# import standard modules
import os
import sys

# import Tora modules
from ConfigReader import ConfigReader
import ToraDB as toradb

TORA_TEMP=".tora/temp"


def object_name(filename, path=TORA_TEMP):
    """
    change the extension of file to object file 
    """
    if not fu.exists(path):
        fu.mkdir(path)

    # trim the original root of file path
    root, leaf = fu.root_leaf(filename)
    filename = leaf

    if ".cpp" in filename: # CPP file
        obj = filename.replace(".cpp", ".o")
        return fu.gen_filepath(path, obj, None)

    if ".CPP" in filename: # CPP file
        obj = filename.replace(".CPP", ".o")
        return fu.gen_filepath(path, obj, None)

    if ".Cpp" in filename: # CPP file
        obj = filename.replace(".Cpp", ".o")
        return fu.gen_filepath(path, obj, None)

    if ".c" in filename: # C file
        obj = filename.replace(".c", ".o")
        return fu.gen_filepath(path, obj, None)

    if ".C" in filename: # C file
        obj = filename.replace(".C", ".o")
        return fu.gen_filepath(path, obj, None)
    
    if ".cuda" in filename: # CUDA file
        obj = filename.replace(".cuda", ".o")
        return fu.gen_filepath(path, obj, None)
    

def compiling_internal_files(reader, path=TORA_TEMP):
    """
    use compiler to compile source file to object file
    """
    source_files = reader.src_list()
    if len(source_files) <= 0:
        raise excepts.InvalidParamException("config file is invalid")

    # create tora db
    database = toradb.create_tora_db()
    if database is None:
        raise excepts.NoAvailableResourcesFoundException("create tora db failed")

    # update each file's md5
    for src in source_files:

        if not toradb.update_tora_hash(src, database):
            continue # file no need to compile

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
        raise excepts.InvalidParamException("params len is not correct")

    # executing
    reader = ConfigReader(sys.argv[1])
    compiling_internal_files(reader)