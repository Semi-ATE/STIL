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
    return os.path.join(str(folder), "stil_files", "header_block", file_name)
        
def test_syn_ok_header_block_1():

    stil_file = get_stil_file("syn_ok_header_block_1.stil")

    parser = STILParser(stil_file)
    tree = parser.parse_syntax()
    if tree == None:
        print("Not expecting FAIL!")
        assert False

def test_syn_err_header_block_1():

    stil_file = get_stil_file("syn_err_header_block_1.stil")

    parser = STILParser(stil_file)
    tree = parser.parse_syntax()
    if tree == None:
        assert parser.err_line == 3
        assert parser.err_col == 8
    else:
        print("Not expecting PASS!")
        assert False

def test_syn_err_header_block_2():

    stil_file = get_stil_file("syn_err_header_block_2.stil")

    parser = STILParser(stil_file)
    tree = parser.parse_syntax()
    if tree == None:
        assert parser.err_line == 3
        assert parser.err_col == 8
    else:
        print("Not expecting PASS!")
        assert False

def test_syn_err_header_block_3():

    stil_file = get_stil_file("syn_err_header_block_3.stil")

    parser = STILParser(stil_file)
    tree = parser.parse_syntax()
    if tree == None:
        assert parser.err_line == 3
        assert parser.err_col == 46
    else:
        print("Not expecting PASS!")
        assert False

def test_syn_err_header_block_4():

    stil_file = get_stil_file("syn_err_header_block_4.stil")

    parser = STILParser(stil_file)
    tree = parser.parse_syntax()
    if tree == None:
        assert parser.err_line == 3
        assert parser.err_col == 46
    else:
        print("Not expecting PASS!")
        assert False

def test_syn_err_header_block_5():

    stil_file = get_stil_file("syn_err_header_block_5.stil")

    parser = STILParser(stil_file)
    tree = parser.parse_syntax()
    if tree == None:
        assert parser.err_line == 3
        assert parser.err_col == 16
    else:
        print("Not expecting PASS!")
        assert False

def test_syn_err_header_block_6():

    stil_file = get_stil_file("syn_err_header_block_6.stil")

    parser = STILParser(stil_file)
    tree = parser.parse_syntax()
    if tree == None:
        assert parser.err_line == 3
        assert parser.err_col == 15
    else:
        print("Not expecting PASS!")
        assert False

def test_syn_err_header_block_7():

    stil_file = get_stil_file("syn_err_header_block_7.stil")

    parser = STILParser(stil_file)
    tree = parser.parse_syntax()
    if tree == None:
        assert parser.err_line == 3
        assert parser.err_col == 17
    else:
        print("Not expecting PASS!")
        assert False

def test_syn_err_header_block_8():

    stil_file = get_stil_file("syn_err_header_block_8.stil")

    parser = STILParser(stil_file)
    tree = parser.parse_syntax()
    if tree == None:
        assert parser.err_line == 3
        assert parser.err_col == 10
    else:
        print("Not expecting PASS!")
        assert False
