#!/bin/env python3
# -*- coding: utf-8 -*-
# Author: Orlando Chen
# Created: Jul 28, 2020
# Modified: Oct 14, 2020


from Tora.Solutions.BasicCompilerParser import BasicCompilerDefined


class XMLDefinedCompiler(BasicCompilerDefined):

    def __init__(self, filename):
        super().__init__(filename)
