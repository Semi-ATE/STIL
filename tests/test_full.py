# -*- coding: utf-8 -*-
import os
import sys

try:
    from Semi_ATE.STIL.parsers.STILParser import STILParser
except:
    cwd = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.insert(0, cwd)
    from Semi_ATE.STIL.parsers.STILParser import STILParser

def get_stil_file(file_name):
    folder = os.path.dirname(__file__)
    return os.path.join(str(folder), "stil_files", file_name)

def test_ok_stil_1():

    stil_file = get_stil_file("test_full.stil")

    # test_full.stil is syntax free stil file, but contains semantic errors
    parser = STILParser(stil_file)
    tree = parser.parse_syntax(debug = False)
    if tree == None:
        assert False

def test_sem_proc_macro_before_pattern_burst():

    stil_file = get_stil_file("test_sem_proc_macro_before_pattern_burst.stil")

    # test_full.stil is syntax free stil file, but contains semantic errors
    parser = STILParser(stil_file)
    tree = parser.parse_syntax(debug = False)
    if tree == None:
        assert False
