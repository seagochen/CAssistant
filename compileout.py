#!/bin/env python3

# import self-defined modules
from convert import ListConvert
from utilities import read_config

# import system standard modules
import os
from os import sys


def search_output(config_dict):
    o_temp = config_dict['temp']['tmp_path']
    o_type = config_dict['gen']['type']
    o_output = config_dict['gen']['output']
    o_compiler = config_dict['gen']['compiler']

    if o_type == 'static':
        return "ar -rcs {} {}/*.o".format(o_output, o_temp)

    if o_type == 'share':
        return "{} -shared -fPIC {}/*.o -o lib{}".format(o_compiler, o_temp, o_output)

    if o_type == 'exe':
        return "{} {}/*.o -o {}".format(o_compiler, o_temp, o_temp)


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
    