#!/bin/env python3
"""
Calling this file will create an empty project
"""

import sys
from siki.basics import FileUtils as fu


def create_empty_project_dir(root_dir):
    
    # create project folder
    fu.mkdir(root_dir)

    # create src folder to holding source files
    src_dir = "{}/src".format(root_dir)
    fu.mkdir(src_dir)

    # copy tora
    tora_dir = fu.gen_folderpath(root_dir, "Tora")
    fu.copy("./Tora", tora_dir)

    # copy Makefile
    makefile = fu.gen_filepath(root_dir, "Makefile")
    fu.copy("./Makefile", makefile)

    # generate an empty project.conf file
    config = fu.gen_filepath(root_dir, "project.conf")
    fu.copy("./project.default.conf", config)


def update_tora_project_config(root_dir):
    
    # remove tora scripts from original project
    tora_dir = fu.gen_folderpath(root_dir, "Tora")
    fu.rmdir(tora_dir)

    # copy new scripts to project
    fu.copy("./Tora", tora_dir)

    # rename old version of Makefile to Makefile.old
    makefile = fu.gen_filepath(root_dir, "Makefile")
    makefile_backup = fu.gen_filepath(root_dir, "Makefile.old")
    fu.move(makefile, makefile_backup)

    # copy new makefile to project
    fu.copy("./Makefile", makefile)

    # rename project.conf file to project.conf.old
    config = fu.gen_filepath(root_dir, "project.conf")
    config_backup = fu.gen_filepath(root_dir, "project.conf.old")
    fu.move(config, config_backup)

    # copy an empty project.conf to project
    fu.copy("./project.default.conf", config)


if __name__ == "__main__":
    
    project_dir = "project"
    if len(sys.argv) >= 2:
        project_dir = sys.argv[1]

    # setup root project dir
    root_dir = "../{}".format(project_dir)

    if fu.exists(root_dir):
        print("Updating the existing tora porject")
        update_tora_project_config(root_dir)
    else:
        print("Creating an empty tora project")
        create_empty_project_dir(root_dir)

    # print out debug message
    print("Done!")