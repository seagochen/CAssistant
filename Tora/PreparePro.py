#!/bin/env python3
"""
Calling this file will create an empty project
"""

from siki.basics import FileUtils as fu


def create_empty_project_dir(folder_name="project"):
    
    # create project folder
    root_dir = "../{}".format(folder_name)
    fu.mkdir(root_dir)

    # create src folder to holding source files
    src_dir = "../{}/src".format(folder_name)
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


if __name__ == "__main__":
    import sys

    project_dir = None
    if len(sys.argv) < 2:
        create_empty_project_dir()
    else:
        create_empty_project_dir(sys.argv[1])

    print("Done!")