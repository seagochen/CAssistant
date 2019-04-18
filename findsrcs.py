#!/bin/env python3

from siki.basics import FileUtils as fu
from siki.basics import SystemUtils as su
from siki.basics.Exceptions import InvalidParamException

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
        cmdls = [config_src['compiler'], _gen_flag(config_src),
        _gen_includes(config_src), f, "-c -o", _gen_tmp_file(config_dict, leaf)]
        cmd = " ".join(cmdls)
        os.system(cmd)


def _gen_flag(config_dict):
    config_flags = config_dict['flags']
    if config_flags is None or len(config_flags) <= 0:
        return ""
    
    # generate flags
    tokens = ListConvert(config_flags).to_list()
    line = ""
    for t in tokens:
        line += "-{} ".format(t[1:-1])
    return line



def _gen_includes(config_dict):
    config_includes = config_dict['includes']
    if config_includes is None or len(config_includes) <= 0:
        return ""
    
    # generate includes
    tokens = ListConvert(config_includes).to_list()
    line = ""
    for t in tokens:
        line += "-I{} ".format(t[1:-1])
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
    

config = read_config()
compile_src_to_temp(config)

# COMPILER = "g++"
# FLAGS = "-std=c++11"
# INCLUDES = ""

# def pre_compile(src):
#     global COMPILER, FLAGS
#     if su.is_linux() or su.is_darwin():
#         cmd = [COMPILER, FLAGS, src, "-c"]
#         os.system(" ".join(cmd))

# def findsrcs():
#     srcs = fu.search_files("./", r"^\./Triangle")
#     for src in srcs:
#         pre_compile(src)


# findsrcs()