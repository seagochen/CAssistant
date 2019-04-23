#!/bin/env python3

# import self-defined modules
from convert import ListConvert

def read_config(config_file="./Tora/project.conf"):
    import configparser
    config = configparser.RawConfigParser()
    config.read(config_file)
    return config


def search_flag(config_dict):
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



def search_includes(config_dict):
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


def search_libraries(config_dict):
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