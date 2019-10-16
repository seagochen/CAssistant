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


def explore_dir_struct(path):
    print(path)
    pass


def copy_headers(config):
    # the includes list from config
    #includes = search_includes(config['src'])
    header_dirs = config['src']['includes']

    print(header_dirs, type(header_dirs))

    # iterate dir struct
    #for dir in includes:
    #    inc_dir = explore_dir_struct(dir)
