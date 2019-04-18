#!/bin/env python3

from siki.basics import FileUtils as fu

import os

from convert import ListConvert

def read_config(config_file="./Tora/project.conf"):
    import configparser
    config = configparser.RawConfigParser()
    config.read(config_file)
    return config


def compile_src_to_temp(config_dict):
    config_src = config_dict['src']
    if len(config_src) <= 0:
        raise InvalidParamException('config is invalid')
    
    flists = fu.search_files(config_src['src_path'], r"\.(c|cpp|cuda)$")
    for f in flists:
        root, leaf = fu.root_leaf(f)
        cmdls = [config_src['compiler'], _search_flag(config_src),
        _search_includes(config_src), f, _search_libraries(config_src), "-c -o", _gen_tmp_file(config_dict, leaf)]
        cmd = " ".join(cmdls)
        # debug
        print("exec:", cmd)
        os.system(cmd)


def _search_flag(config_dict):
    config_flags = config_dict['flags']
    if config_flags is None or len(config_flags) <= 0:
        return ""
    
    # generate flags
    tokens = ListConvert(config_flags).to_list()
    if tokens is None:
        return ""
    
    # generate tokens
    line = ""
    for t in tokens:
        line += "-{} ".format(t[1:-1])
    return line



def _search_includes(config_dict):
    config_includes = config_dict['includes']
    if config_includes is None or len(config_includes) <= 0:
        return ""
    
    # generate includes
    tokens = ListConvert(config_includes).to_list()
    if tokens is None:
        return ""

    # generate tokens
    line = ""
    for t in tokens:
        line += "-I{} ".format(t[1:-1])
    return line


def _search_libraries(config_dict):
    config_libs = config_dict['libraries']
    if config_libs is None or len(config_libs) <= 0:
        return ""
    
    # generate includes
    tokens = ListConvert(config_libs).to_list()
    if tokens is None:
        return ""

    # generate tokens
    line = ""
    for t in tokens:
        line += "-l{} ".format(t[1:-1])
    return line


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
    config = read_config()
    compile_src_to_temp(config)