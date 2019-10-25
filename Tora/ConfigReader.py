#!/bin/env python3
"""
This file reads configuration file
"""

class ListConvert(object):
    """
    This module can convert a string with the format 
    ['a', 'b', 'c'] or ["a", "b", "c"] to a list object 
    of python: [a, b, c]
    """

    def __init__(self, strdict):
        self.strdict = strdict

    def _valid(self):
        import re
        pattern_dq = r"^\[((\".+\")\s{0,},\s{0,}){0,}(\".+\")\s{0,}\]$"
        pattern_sq = r"^\[((\'.+\')\s{0,},\s{0,}){0,}(\'.+\')\s{0,}\]$"
        ret1 = re.match(pattern_dq, self.strdict)
        ret2 = re.match(pattern_sq, self.strdict)
        return ret1 or ret2


    def to_list(self):
        if self.strdict is None or len(self.strdict) <= 0:
            return None

        if self._valid() is None:
            return None

        # trim the string first
        self.strdict = self.strdict.replace(" ", "")
        
        # trim the barackets
        strdict = self.strdict[1:-1]

        # split the string
        tokens = strdict.split(',')
        return tokens


import siki.basics.Exceptions as excepts
import siki.basics.FileUtils as fu

class ConfigReader(object):
    """
    This module can read the required parameters 
    from the configuration file.
    """

    def __init__(self, config_file):
        import configparser

        if config_file is None:
            raise excepts.NullPointerException("configure file path could be null")

        config = configparser.RawConfigParser()
        config.read(config_file)

        self.config = config


    def compiler(self):
        return self.config['conf']['compiler']

    def sys_libs(self):
        tokens = ListConvert(self.config['conf']['sys_libs']).to_list()
        
        if tokens is None or len(tokens) <= 0:
            return ""
        
        line = ""
        for token in tokens:
            line += "-l{} ".format(token[1:-1])

        return line


    def dir_libs(self):
        dir_path = ListConvert(self.config['conf']['dir_libs']).to_list()

        if dir_path is None or len(dir_path) <= 0:
            return ""

        dirs = []
        for path in dir_path:
            dirs.append(path[1:-1])
        
        a_files = []
        for dirlib in dirs:
            files = fu.search_files(dirlib, "\.a$")
            if len(files) > 0:
                a_files.extend(files)

        return " ".join(a_files)


    def file_libs(self):
        flibs = ListConvert(self.config['conf']['file_libs']).to_list()

        if flibs is None or len(flibs) <= 0:
            return ""

        temp = []
        for lib in flibs:
            temp.append(lib[1:-1])
        
        return " ".join(temp)


    def include_list(self):
        inc_headers = ListConvert(self.config['conf']['includes']).to_list()

        if inc_headers is None or len(inc_headers) <= 0:
            return []

        flist = []
        for token in inc_headers:
            flist.append(token[1:-1])

        return flist    

    
    def includes(self):
        line = ""
        for token in self.include_list():
            line += "-I{} ".format(token)
        
        return line

    
    def src_list(self):
        source_pathes = ListConvert(self.config['src']['src_path']).to_list()

        if source_pathes is None or len(source_pathes) <= 0:
            return ""

        files = []
        for path in source_pathes:
            source_files = fu.search_files(path[1:-1], 
                r"\.(c|cpp|cuda|C|CPP|Cpp)$")

            if source_files is None or len(source_files) <= 0:
                continue

            files.extend(source_files)

        return files


    def src_flags(self):
        flags = ListConvert(self.config['src']['flags']).to_list()

        if flags is None or len(flags) <= 0:
            return ""

        # generate tokens
        line = ""
        for t in flags:
            line += "-{} ".format(t[1:-1])
        return line  

    def src_macros(self):
        macros = ListConvert(self.config['src']['macros']).to_list()

        if macros is None or len(macros) <= 0:
            return ""

        # generate tokens
        line = ""
        for t in macros:
            line += "-D{} ".format(t[1:-1])
        return line          


    def gen_type(self):
        return self.config['gen']['type']

    def gen_name(self):
        if self.gen_type() == "exe":
            return self.config['gen']['name']
        elif self.gen_type() == "share":
            return "lib{}.so".format(self.config['gen']['name'])
        elif self.gen_type() == "static":
            return "lib{}.a".format(self.config['gen']['name'])
        else:
            raise excepts.InvalidParamException("Invalid generated file type")

    def gen_flags(self):
        flags = ListConvert(self.config['gen']['flags']).to_list()

        if flags is None or len(flags) <= 0:
            return ""

        # generate tokens
        line = ""
        for t in flags:
            line += "-{} ".format(t[1:-1])
        return line

    def gen_output_dir(self):
        return self.config['gen']['output_dir']


# for debug and unit test
if __name__ == "__main__":
    reader = ConfigReader("project.conf")
    print(reader.compiler())
    print(reader.sys_libs())
    print(reader.dir_libs())
    print(reader.file_libs())
    print(reader.includes())
    print(reader.src_list())
    print(reader.src_flags())
    print(reader.src_macros())
    print(reader.gen_type())
    print(reader.gen_flags())
    print(reader.gen_name())
    print(reader.gen_output_dir())