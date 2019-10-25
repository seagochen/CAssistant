#!/bin/env python3
"""
This file provides Tora clean methods
"""

# import siki
from siki.basics import FileUtils as fu
from siki.basics.Exceptions import *

# import standard modules
import os
import sys

# import self-defined modules
from utilities import read_config

def clean_temp_files(config):
    if config is None:
        raise InvalidParamException('config is invalid')
    
    tempdir = config["temp"]["tmp_path"]

    if tempdir is None:
        raise InvalidParamException('config is invalid') 

    # find all files under temp dir
    flists = fu.search_files(tempdir)

    # remove files in temp dir
    for f in flists:
        print("rm: {}".format(f))
        fu.rmfile(f)

    # remove filetering database
    if fu.exists(config['conf']['toradb']):
        fu.rmfile(config['conf']['toradb'])


def clean_gen_file(config):
    if config is None:
        raise InvalidParamException('config is invalid')

    # find the file name
    outputs = search_output(config)

    # # executing
    if outputs is None or len(outputs) <= 0:
        return

    for f in outputs:
        print("rm {}".format(f))
        fu.rmfile(f)


def search_output(config):
    otype = config["gen"]["type"]
    fname = config["gen"]["output"]
    flist = None

    if otype == "exe":
        flist = fu.search_files("./", "{}\\.exe$".format(fname))
        # print(flist)
    elif otype == "share":
        flist = fu.search_files("./", "{}\\.so$".format(fname))
        # print(flist)
    elif otype == "static":
        flist = fu.search_files("./", "{}\\.a$".format(fname))
        # print(flist) 

    return flist      




if __name__ == "__main__":
    """
    usage: python3 cleanpro.py path_of_config_file command
    command> 
        temp    - clean temporary files
        gen     - clean generated file
    """

    # if script with arguments
    config = None
    if len(sys.argv) >= 2:
        config = read_config(sys.argv[1])
    else:
        config = read_config()

    # executing
    if len(sys.argv) == 3:
        cmd = sys.argv[2]

        if cmd == "temp":
            clean_temp_files(config)
        elif cmd == "gen":
            clean_gen_file(config)
    else: # default
        clean_temp_files(config)
        clean_gen_file(config)

    
