#!/bin/env python3
"""
This file is trying to compile the obj-file to final code
"""
# import siki
from siki.basics import Exceptions

# import system standard modules
import os
import sys

# import Tora modules
from ConfigReader import ConfigReader

TORA_TEMP=".tora/temp"

def generate_final(reader, path=TORA_TEMP):
    if reader.gen_type() == 'static':
        cmd = "ar -rcs {} {} {}/*.o".format(
            reader.gen_name(),  # generate file name
            reader.ext_libs(),  # external libs
            # reader.dir_libs(),  # dir libs
            # reader.file_libs(), # file libs
            path                # temp files
        )
        print("exec:", cmd)
        os.system(cmd)
    
    if reader.gen_type() == 'share':
        cmd = "{} -shared -fPIC {} {}/*.o -o {}".format(
            reader.compiler(),  # compiler
            reader.ext_libs(),  # external libs
            # reader.dir_libs(),  # dir libs
            # reader.file_libs(), # file libs
            path,               # temp files
            reader.gen_name()   # generate file name
        )
        print("exec:", cmd)
        os.system(cmd)
    
    if reader.gen_type() == 'exe':
        cmd = "{} {} -o {} {}/*.o {} {}".format(
            reader.compiler(),  # compiler
            reader.gen_flags(), # compile flags
            reader.gen_name(),  # generate file name
            path,               # temp files
            reader.sys_libs(),  # system libs
            # reader.dir_libs(),  # dir libs
            # reader.file_libs()  # file libs
            reader.ext_libs()
        )
        print("exec:", cmd)
        os.system(cmd)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise Exceptions.InvalidParamException("params len is not correct")

    # executing
    reader = ConfigReader(sys.argv[1])
    generate_final(reader)