#!/bin/env python3

# import siki
from siki.basics import FileUtils as fu
from siki.basics.Exceptions import *

# import standard modules
import os
import sys

# import self-defined modules
from utilities import read_config

def clean_path(config):
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


def clean_output(config):
    if config is None:
        raise InvalidParamException('config is invalid')

    output = config["gen"]["output"]

    if output is None:
        raise InvalidParamException('config is invalid')

    # find the file name
    outputs = clean_filename(output)

    # executing
    for f in outputs:
        print("rm : {}".format(f))
        cmd = "rm {}".format(f)
        os.system(cmd)


def clean_filename(filename):
    flist = fu.search_files("./", filename)
    if len(flist) > 0:
        return flist
    else:
        return None


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
            clean_path(config)
        elif cmd == "gen":
            clean_output(config)
    else: # default
        clean_path(config)
        clean_output(config)

    
