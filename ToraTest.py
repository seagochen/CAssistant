# from Tora.XmlParser.SolutionParser import SolutionParser
from Tora.Compiler.GCC import GCC

compiler = GCC("./solution.xml")
compiler.gen_objects()
