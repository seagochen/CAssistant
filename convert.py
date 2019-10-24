#!/bin/env python3
"""
This file provides a class which could convert a string with
the format ['a', 'b', 'c'] or ["a", "b", "c"] to a list object 
of python
"""

# import standard
import re

# import siki
from siki.basics.Exceptions import CannotParseException

class ListConvert(object):
    """
    This module can convert a string with the format 
    ['a', 'b', 'c'] or ["a", "b", "c"] to a list object 
    of python
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
        if self._valid() is None:
            return None

        if self.strdict is None or len(self.strdict) <= 0:
            return None

        # trim the string first
        self.strdict = self.strdict.replace(" ", "")
        
        # trim the barackets
        strdict = self.strdict[1:-1]

        # split the string
        tokens = strdict.split(',')
        return tokens
