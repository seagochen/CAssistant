#!/bin/env python3
"""
Calling this file will create an empty project
"""

import sys
from siki.basics import FileUtils


def create_empty_project_dir(root_dir):
    
    # create project folder
    FileUtils.mkdir(root_dir)

    # create src folder to holding source files
    src_dir = "{}/src".format(root_dir)
    FileUtils.mkdir(src_dir)

    # copy tora
    tora_dir = FileUtils.gen_folder_path(root_dir, "Tora")
    FileUtils.copy("./Tora", tora_dir)

    # copy Makefile
    makefile = FileUtils.gen_file_path(root_dir, "Makefile")
    FileUtils.copy("./Makefile", makefile)

    # generate an empty project.conf file
    config = FileUtils.gen_file_path(root_dir, "project.conf")
    FileUtils.copy("./project.default.conf", config)


def update_tora_project_config(root_dir):
    
    # remove tora scripts from original project
    tora_dir = FileUtils.gen_folder_path(root_dir, "Tora")
    FileUtils.rmdir(tora_dir)

    # copy new scripts to project
    FileUtils.copy("./Tora", tora_dir)

    # rename old version of Makefile to Makefile.old
    makefile = FileUtils.gen_file_path(root_dir, "Makefile")
    makefile_backup = FileUtils.gen_file_path(root_dir, "Makefile.old")
    FileUtils.move(makefile, makefile_backup)

    # copy new makefile to project
    FileUtils.copy("./Makefile", makefile)

    # rename project.conf file to project.conf.old
    config = FileUtils.gen_file_path(root_dir, "project.conf")
    config_backup = FileUtils.gen_file_path(root_dir, "project.conf.old")
    FileUtils.move(config, config_backup)

    # copy an empty project.conf to project
    FileUtils.copy("./project.default.conf", config)


if __name__ == "__main__":
    
    project_dir = "project"
    if len(sys.argv) >= 2:
        project_dir = sys.argv[1]

    # setup root project dir
    root_dir = "../{}".format(project_dir)

    if FileUtils.exists(root_dir):
        print("Updating exsiting tora project...")
        update_tora_project_config(root_dir)
    else:
        print("Creating an empty tora project...")
        create_empty_project_dir(root_dir)

    # print out debug message
    print("Done!")
