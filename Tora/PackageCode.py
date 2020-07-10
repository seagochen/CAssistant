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
from siki.basics import FileUtils
from siki.basics import Hashcode
from siki.basics import Exceptions


def copy_files(old_path, new_path):
    if FileUtils.exists(new_path):  # compute hash code
        hash_new = Hashcode.compute_file_md5(new_path)
        hash_old = Hashcode.compute_file_md5(old_path)

        if hash_old == hash_new:  # same file
            return None  # do nothing

    # mkdir if not exists
    head, tail = ntpath.split(new_path)
    if not FileUtils.exists(head):
        FileUtils.mkdir(head)

    # copy file if not exists or out of date
    print("copy {} to {}".format(old_path, new_path))
    FileUtils.copy(old_path, new_path)


def copy_folder(hdir, outputdir):
    # search header files
    hdir_flist = FileUtils.search_files(hdir, r"\.(h|hpp|H|HPP|Hpp)$")

    if len(hdir_flist) <= 0:  # nothing need to do
        return None

    if not FileUtils.exists(outputdir):  # create folder if need
        FileUtils.mkdir(outputdir)

    for f in hdir_flist:  # copy header files to the folder

        # trim relative path symbols
        if f.startswith("../"):
            f = f[3:]
        elif f.startswith("./"):
            f = f[2:]

        # copy files
        target_path = FileUtils.gen_file_path(outputdir, f)
        copy_files(f, target_path)


def copy_if_need(conf_reader):
    packages = conf_reader.package_dirs()

    if len(packages) <= 0:
        return  # nothing to do

    for path in packages:
        if not FileUtils.exists(path):  # folder path is not exists
            print("cannot copy {} to {}, because {} not exists".format(
                path, conf_reader.gen_output_dir(), path
            ))
            continue

        # copy folder with headers to destination
        copy_folder(path, conf_reader.gen_output_dir())


def move_generate(conf_reader):
    if not FileUtils.exists(conf_reader.gen_output_dir()):
        FileUtils.mkdir(conf_reader.gen_output_dir())

    if FileUtils.exists(conf_reader.gen_name()):
        # delete if exists
        file_path = FileUtils.gen_file_path(conf_reader.gen_output_dir(), conf_reader.gen_name())
        if FileUtils.exists(file_path):
            FileUtils.rmfile(file_path)

        # copy generated file to the folder
        FileUtils.move(conf_reader.gen_name(), conf_reader.gen_output_dir())


if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise Exceptions.InvalidParamException("params len is not correct")

    # move generate to folder
    reader = ConfigReader(sys.argv[1])
    move_generate(reader)

    # copy headers to folder
    if reader.gen_type() == 'share' or reader.gen_type() == 'static':
        copy_if_need(reader)
