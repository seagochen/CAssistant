#!/bin/env python3

# import self-defined modules
from convert import ListConvert
from utilities import *

# import system standard modules
import os
import sys

def search_output(config_dict):
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
    