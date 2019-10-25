#!/bin/env python3
"""
The module provides a packaging method, and when the file type is
library, the module is in charge of packaging and generating the required.

Or just normally move the output file to the required folder
"""

# import standard libraries
import os
import sys
import ntpath

# import tora modules
from ConfigReader import ConfigReader

# import siki
from siki.basics import FileUtils as fu
from siki.basics import Hashcode as hcode


def move_generate(reader):
    if not fu.exists(reader.gen_output_dir()):
        fu.mkdir(reader.gen_output_dir())

    if fu.exists(reader.gen_name()):
        # delete if exists
        filepath = fu.gen_filepath(reader.gen_output_dir(), reader.gen_name())
        if fu.exists(filepath):
            fu.rmfile(filepath)

        # copy generated file to the folder
        fu.move(reader.gen_name(), reader.gen_output_dir())


def create_folder_and_copy_if_necessary(old_path, new_path):

    if fu.exists(new_path): # compute hash code
        hash_new = hcode.compute_file_md5(new_path)
        hash_old = hcode.compute_file_md5(old_path)

        if hash_old == hash_new: # same file
            return None # do nothing

    # mkdir if not exists
    head, tail = ntpath.split(new_path)
    if not fu.exists(head):
        fu.mkdir(head)

    # copy file if not exists or out of date
    print("copy {} to {}".format(old_path, new_path))
    fu.copy(old_path, new_path)


def copy_headers(hdir, outputdir):
    # search header files
    hdir_flist = fu.search_files(hdir, r"\.(h|hpp|H|HPP|Hpp)$")

    # nothing need to do
    if len(hdir_flist) <= 0:
        return None

    if not fu.exists(outputdir):
        fu.mkdir(outputdir)
    
    # copy header files to the folder
    for f in hdir_flist:
        target_path = fu.gen_filepath(outputdir, f)
        create_folder_and_copy_if_necessary(f, target_path)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise excepts.InvalidParamException("params len is not correct")

    # move generate to folder
    reader = ConfigReader(sys.argv[1])
    move_generate(reader)

    # copy headers to folder
    if reader.gen_type() == 'share' or reader.gen_type() == 'static':
        for hdir in reader.include_list():
            copy_headers(hdir, reader.gen_output_dir())