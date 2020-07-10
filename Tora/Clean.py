#!/bin/env python3
"""
This file provides Tora clean methods
"""

# import siki
from siki.basics import FileUtils
from siki.basics import Exceptions

# import standard modules
import os
import sys

# import tora modules
from ConfigReader import ConfigReader 

TORA_TEMP=".tora"


def clean_temp_files(path=TORA_TEMP):
    if not FileUtils.exists(path):
        return None

    os.system("rm -rf {}".format(path))
    print("temporaries cleaned")


def clean_gen_file(reader):
    if not FileUtils.exists(reader.gen_output_dir()):
        return None

    os.system("rm -rf {}".format(reader.gen_output_dir()))
    print("output dir cleaned")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise Exceptions.InvalidParamException("params len is not correct")

    reader = ConfigReader(sys.argv[1])

    # clean temporaries
    clean_temp_files()

    # clean generated file
    clean_gen_file(reader)

    # message done
    print("done!")