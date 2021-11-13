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
    print(f"Testing {file_name}")
    return os.path.join(str(folder), "stil_files", "stil_block", file_name)
    
def test_syn_ok_stil_block_1():
    
    stil_file = get_stil_file("syn_ok_stil_block_1.stil")

    parser = STILParser(stil_file)
    tree = parser.parse_syntax()
    if tree == None:
        print("Not expecting FAIL!")
        assert False

    
def test_syn_err_stil_block_1():
    
    stil_file = get_stil_file("syn_err_stil_block_1.stil")

    parser = STILParser(stil_file)
    tree = parser.parse_syntax()
    if tree == None:
        assert parser.err_line == 1
        assert parser.err_col == 1
    else:
        print("Not expecting PASS!")
        assert False

def test_syn_err_stil_block_2():

    stil_file = get_stil_file("syn_err_stil_block_2.stil")

    parser = STILParser(stil_file)
    tree = parser.parse_syntax()
    if tree == None:
        assert parser.err_line == 1
        assert parser.err_col == 5
    else:
        print("Not expecting PASS!")
        assert False

def test_syn_err_stil_block_3():

    stil_file = get_stil_file("syn_err_stil_block_3.stil")

    parser = STILParser(stil_file)
    tree = parser.parse_syntax()
    if tree == None:
        assert parser.err_line == 1
        assert parser.err_col == 6
    else:
        print("Not expecting PASS!")
        assert False

def test_syn_err_stil_block_4():

    stil_file = get_stil_file("syn_err_stil_block_4.stil")

    parser = STILParser(stil_file)
    tree = parser.parse_syntax()
    if tree == None:
        assert parser.err_line == 1
        assert parser.err_col == 6
    else:
        print("Not expecting PASS!")
        assert False

def test_syn_err_stil_block_5():

    stil_file = get_stil_file("syn_err_stil_block_5.stil")

    parser = STILParser(stil_file)
    tree = parser.parse_syntax()
    if tree == None:
        assert parser.err_line == 1
        assert parser.err_col == 6
    else:
        print("Not expecting PASS!")
        assert False

def test_syn_err_stil_block_6():

    stil_file = get_stil_file("syn_err_stil_block_6.stil")

    parser = STILParser(stil_file)
    tree = parser.parse_syntax()
    if tree == None:
        assert parser.err_line == 1
        assert parser.err_col == 11
    else:
        print("Not expecting PASS!")
        assert False

def test_syn_err_stil_block_7():

    stil_file = get_stil_file("syn_err_stil_block_7.stil")

    parser = STILParser(stil_file)
    tree = parser.parse_syntax()
    if tree == None:
        assert parser.err_line == 1
        assert parser.err_col == 12
    else:
        print("Not expecting PASS!")
        assert False

def test_syn_err_stil_block_8():

    stil_file = get_stil_file("syn_err_stil_block_8.stil")

    parser = STILParser(stil_file)
    tree = parser.parse_syntax()
    if tree == None:
        assert parser.err_line == 1
        assert parser.err_col == 19
    else:
        print("Not expecting PASS!")
        assert False

def test_syn_err_stil_block_9():

    stil_file = get_stil_file("syn_err_stil_block_9.stil")

    parser = STILParser(stil_file)
    tree = parser.parse_syntax()
    if tree == None:
        assert parser.err_line == 1
        assert parser.err_col == 40
    else:
        print("Not expecting PASS!")
        assert False

def test_syn_err_stil_block_10():

    stil_file = get_stil_file("syn_err_stil_block_10.stil")

    parser = STILParser(stil_file)
    tree = parser.parse_syntax()
    if tree == None:
        assert parser.err_line == 1
        assert parser.err_col == 25
    else:
        print("Not expecting PASS!")
        assert False

def test_sem_err_stil_block_1():
    
    stil_file = get_stil_file("sem_err_stil_block_1.stil")

    parser = STILParser(stil_file)
    tree = parser.parse_syntax()
    parser.parse_semantic(tree)
    if tree == None:
        print("Not expecting ERROR!")
        assert False
    assert parser.err_line == 1
    assert parser.err_col == 6

def test_sem_err_stil_block_2():
    
    stil_file = get_stil_file("sem_err_stil_block_2.stil")

    parser = STILParser(stil_file)
    tree = parser.parse_syntax()
    parser.parse_semantic(tree)
    if tree == None:
        print("Not expecting ERROR!")
        assert False
    assert parser.err_line == 2
    assert parser.err_col == 12

def test_sem_err_stil_block_3():
    
    stil_file = get_stil_file("sem_err_stil_block_3.stil")

    parser = STILParser(stil_file)
    tree = parser.parse_syntax()
    parser.parse_semantic(tree)
    if tree == None:
        print("Not expecting ERROR!")
        assert False
    assert parser.err_line == 2
    assert parser.err_col == 14
