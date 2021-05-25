# -*- coding: utf-8 -*-
import os
from Semi_ATE.STIL.parsers.STILParser import STILParser

def get_stil_file(file_name):
    folder = os.path.dirname(__file__)
    return os.path.join(str(folder), "stil_files", file_name)

def test_ok_stil_1():

    stil_file = get_stil_file("test_full.stil")

    parser = STILParser()
    tree = parser.parse_syntax(stil_file, debug = False)
    if tree == None:
        assert False
