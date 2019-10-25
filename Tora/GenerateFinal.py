#!/bin/env python3
"""
This file is trying to compile the obj-file to final code
"""
# import siki
from siki.basics import FileUtils as fu

# import system standard modules
import os
import sys

# import Tora modules
from ConfigReader import ConfigReader

TORA_TEMP=".tora/temp"

def generate_final(reader, path=TORA_TEMP):
    if reader.gen_type() == 'static':
        cmd = "ar -rcs {} {}/*.o".format(
            reader.gen_name(),
            path
        )
        print("exec:", cmd)
        os.system(cmd)
    
    if reader.gen_type() == 'share':
        cmd = "{} -shared -fPIC {}/*.o -o {}".format(
            reader.compiler(),
            path,
            reader.gen_name()
        )
        print("exec:", cmd)
        os.system(cmd)
    
    if reader.gen_type() == 'exe':
        cmd = "{} {} {} {} {} {}/*.o -o {}".format(
            reader.compiler(),
            reader.gen_flags(),
            reader.sys_libs(),
            reader.dir_libs(),
            reader.file_libs(),
            path,
            reader.gen_name()
        )
        print("exec:", cmd)
        os.system(cmd)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise excepts.InvalidParamException("params len is not correct")

    # executing
    reader = ConfigReader(sys.argv[1])
    generate_final(reader)