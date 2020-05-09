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

def copy_files(old_path, new_path):

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


def copy_folder(hdir, outputdir):

    # search header files
    hdir_flist = fu.search_files(hdir, r"\.(h|hpp|H|HPP|Hpp)$")

    if len(hdir_flist) <= 0: # nothing need to do
        return None

    if not fu.exists(outputdir): # create folder if need
        fu.mkdir(outputdir)
    
    for f in hdir_flist: # copy header files to the folder

        # trim relative path symbols
        if f.startswith("../"):
            f = f[3:]
        elif f.startswith("./"):
            f = f[2:]

        # copy files
        target_path = fu.gen_filepath(outputdir, f)
        copy_files(f, target_path)


def copy_if_need(reader):
    packages = reader.package_dirs()

    if len(packages) <= 0:
        return # nothing to do
    
    for path in packages:
        if not fu.exists(path): # folder path is not exists
            print("cannot copy {} to {}, because {} not exists".format(
                path, reader.gen_output_dir(), path
            ))
            continue
        
        # copy folder with headers to destination
        copy_folder(path, reader.gen_output_dir())


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


if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise excepts.InvalidParamException("params len is not correct")

    # move generate to folder
    reader = ConfigReader(sys.argv[1])
    move_generate(reader)

    # copy headers to folder
    if reader.gen_type() == 'share' or reader.gen_type() == 'static':
        copy_if_need(reader)