#!/bin/env python3
"""
This file is trying to compile the obj-file to final code
"""

# import self-defined modules
from convert import ListConvert
from utilities import *
from dirstruct import copy_headers

# import siki
from siki.basics import FileUtils as fu

# import system standard modules
import os
import sys

def search_output(config_dict):
    """
    search output configuration and generate final command
    """
    tempdir = config_dict['temp']['tmp_path']
    outtype = config_dict['gen']['type']
    outname = config_dict['gen']['output']
    compiler = config_dict['gen']['compiler']

    if outtype == 'static':
        return "ar -rcs {}.a {}/*.o".format(outname, tempdir)

    if outtype == 'share':
        return "{} -shared -fPIC {}/*.o -o lib{}.so".format(compiler, tempdir, outname)

    if outtype == 'exe':
        gendict = config_dict['gen']
        additions = [search_flag(gendict), search_libraries(gendict), search_files(gendict)]
        additions = " ".join(additions)
        return "{} {}/*.o {} -o {}.exe".format(compiler, tempdir, additions, outname)


def move_gen(filename, projdir):
    # move generated file to the desired dir
    # liveMedia.a projdir
    if not fu.exists(projdir):
        fu.mkdir(projdir)
    
    # move the output file to the folder
    output = fu.gen_filepath(projdir, filename)
    
    # check if file exists, remove it first
    if fu.exists(output):
        fu.rmfile(output)
    
    # just move generated file to the folder
    fu.move(filename, projdir)


def gen_final(config_dict):
    """
    put generated files and its relatives to the target folder
    """
    projdir = config_dict['gen']['projdir']
    outtype = config_dict['gen']['type']
    outname = config_dict['gen']['output']
    
    # check dir is exits
    if not os.path.isdir(projdir):
        fu.mkdir(projdir)
    
    # change the output file extension
    if outtype == "static":
        outname = "{}.a".format(outname)
    elif outtype == "share":
        outname = "{}.so".format(outname)
    elif outtype == "exe":
        outname = "{}.exe".format(outname)
    
    # move the generated file to folder
    move_gen(outname, projdir)

    # if generated is library, still need to copy its
    # header files and its dir to output dir
    copy_headers(config_dict)


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
    cmd = search_output(config)
    print("exec:", cmd)
    os.system(cmd)

    # output necessary files to the dir folder
    gen_final(config)
    
