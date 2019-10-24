#!/bin/env python3
"""
This file uses the structure FileNodeTree to help
header files copying
"""

from utilities import search_includes
from siki.basics import FileUtils as fu
from siki.basics import Hashcode as hcode

from convert import ListConvert
from FileNodeTree import FileNodeTree
import FileTreeUtils as ftree
import ntpath


def create_folder_and_copy_if_necessary(old_path, new_path):

    print("copy {} to {}".format(old_path, new_path))

    if fu.exists(new_path): # compute hash code
        hash_new = hcode.compute_file_md5(new_path)
        hash_old = hcode.compute_file_md5(old_path)

        if hash_old == hash_new: # same file
            pass # do nothing

    # mkdir if not exists
    head, tail = ntpath.split(new_path)
    if not fu.exists(head):
        fu.mkdir(head)

    # copy file if not exists or out of date
    fu.copy(old_path, new_path)


def copy_headers_if_necessary(header_dirs, output_dir):
    """
    @param header_dirs: headers dirs to export
    @param output: output_dir
    """
    
    # search include header files directories
    h_dirs = ListConvert(header_dirs).to_list() 
    for i in range(len(h_dirs)):
        h_dirs[i] = h_dirs[i][1:-1]
    
    # search and list out all necessary
    # header files under the given folder
    current_headers_dir = FileNodeTree(".")

    for h_dir in h_dirs:
        tree = ftree.traversal_dir(h_dir, r"\.[h|hpp|H|Hpp|HPP]$")

        # add trees to current header tree
        if len(tree.only_files()) > 0:
            current_headers_dir.append_node(tree)

    # list all headers from tree
    origin_files_list = current_headers_dir.only_files()
    
    # create a copy
    output_headers_dir = ftree.copy_tree(current_headers_dir)
    target_nodes_list = output_headers_dir.only_files(True)

    # change the output dir to target
    output_headers_dir.name = output_dir

    target_files_list = []
    for node in target_nodes_list:
        target_files_list.append(node.generate_path())

    # copy files
    if len(origin_files_list) == len(target_files_list):    
        for i in range(len(target_files_list)):
            create_folder_and_copy_if_necessary(origin_files_list[i],
                target_files_list[i])


def copy_headers(config):
    # the includes list from config
    header_dirs = config['src']['includes']
    output_dir = config['gen']['projdir']
    output_type = config['gen']['type']

    if output_type == "exe": # just output the executable file
        pass

    print("Tora is trying to copy a backup of headers to the same folder")
    # else, iterate directory and list all header files
    # and copy them to the output dir
    copy_headers_if_necessary(header_dirs, output_dir)
