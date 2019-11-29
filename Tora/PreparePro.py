#!/bin/env python3
"""
Calling this file will create an empty project
"""

from siki.basics import FileUtils as fu


def create_empty_project_dir(folder_name="project"):
    # create src folder to holding source files
    # copy tora
    # copy Makefile
    # generate an empty project.conf file
    pass




if __name__ == "__main__":
    import sys

    project_dir = None
    if len(sys.argv) < 2:
        create_empty_project_dir()
    else:
        create_empty_project_dir(sys.argv[1])

    print("Done!")