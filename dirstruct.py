#!/bin/env python3
"""
It will try to create a file structure consistent with the source code structure to hold the required header files
"""

from utilities import search_includes
from siki.basics.FileUtils import mkdir, search_folders, search_files

class TreeNode(object):
    """The basic node of tree structure"""

    def __init__(self, name, parent=None):
        super(TreeNode, self).__init__()
        self.name = name
        self.parent = parent
        self.child = {}

    def __repr__(self) :
        return 'TreeNode(%s)' % self.name

    def get_child(self, name, defval=None):
        """get a child node of current node"""
        return self.child.get(name, defval)

    def add_child(self, name, obj=None):
        """add a child node to current node"""
        if obj and not isinstance(obj, TreeNode):
            raise ValueError('TreeNode only add another TreeNode obj as child')
        if obj is None:
            obj = TreeNode(name)
        obj.parent = self
        self.child[name] = obj
        return obj

    def del_child(self, name):
        """remove a child node from current node"""
        if name in self.child:
            del self.child[name]

    def find_child(self, path, create=False):
        """find child node by path/name, return None if not found"""
        # convert path to a list if input is a string
        path = path if isinstance(path, list) else path.split()
        cur = self
        for sub in path:
            # search
            obj = cur.get_child(sub)
            if obj is None and create:
                # create new node if need
                obj = cur.add_child(sub)
            # check if search done
            if obj is None:
                break
            cur = obj
        return obj


def explore_header_files_if_necessary(path):
    from convert import ListConvert
    
    # header-related dirs
    tokens = ListConvert(path).to_list()
    for i in range(len(tokens)):
        tokens[i] = tokens[i][1:-1]

    # list out all header files under the given folder
    f_output = []
    for fdir in tokens:
        out = search_files(fdir, r"\.[h|hpp|H|Hpp|HPP]")
        if len(out) > 0: # find out something
            f_output.extend(out)
    
    # print out for debug
    #print(f_output)

    # generate file tree



def copy_headers(config):
    # the includes list from config
    header_dirs = config['src']['includes']

    # iterate directory and list all header files
    explore_header_files_if_necessary(header_dirs)
