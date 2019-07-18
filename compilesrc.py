#!/bin/env python3

# import siki
from siki.basics import FileUtils as fu
from siki.basics.Exceptions import *

# import standard modules
import os
import sys

# import self-defined modules
from convert import ListConvert
from utilities import *


def compile_src_to_temp(config_dict):
    config_src = config_dict['src']
    if len(config_src) <= 0:
        raise InvalidParamException('config is invalid')
    
    # convert src path to list
    pathes = ListConvert(config_src['src_path']).to_list()

    # iterate every path
    for path in pathes:
        flists = fu.search_files(path[1:-1], r"\.(c|cpp|cuda)$")
        for f in flists:
            root, leaf = fu.root_leaf(f)
            cmdls = [config_src['compiler'], search_flag(config_src),
            search_includes(config_src), f, search_libraries(config_src), "-c -o", _gen_tmp_file(config_dict, leaf)]
            cmd = " ".join(cmdls)
            # debug
            print("exec:", cmd)
            os.system(cmd)


def _gen_tmp_file(config_dict, srcfile):
    tmp_config = config_dict['temp']
    tmp_dir = tmp_config['tmp_path']

    if tmp_dir is None:
        fu.mkdir('tmp')
        tmp_dir = 'tmp'
    else:
        fu.mkdir(tmp_dir)

    if ".cpp" in srcfile:
        obj = srcfile.replace(".cpp", ".o")
        return fu.gen_filepath(tmp_dir, obj, None)
    if ".c" in srcfile:
        obj = srcfile.replace(".c", ".o")
        return fu.gen_filepath(tmp_dir, obj, None)
    

if __name__ == "__main__":
    """
    usage: python3 cleanpro.py path_of_config_file command
    """

    # if script with arguments
    config = None
    if len(sys.argv) >= 2:
        config = read_config(sys.argv[1])
    else:
        config = read_config()

    # executing
    compile_src_to_temp(config)