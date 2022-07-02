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
    return os.path.join(str(folder), "stil_files", "spec_block", file_name)


def test_syn_err_spec_block_1():
    stil_file = get_stil_file("syn_err_spec_block_1.stil")

    parser = STILParser(stil_file)
    parser.parse_syntax()
    assert parser.err_line == 23
    assert parser.err_col == 6

def test_syn_err_spec_block_2():
    stil_file = get_stil_file("syn_err_spec_block_2.stil")

    parser = STILParser(stil_file)
    parser.parse_syntax()
    assert parser.err_line == 23
    assert parser.err_col == 18

def test_syn_err_spec_block_3():
    stil_file = get_stil_file("syn_err_spec_block_3.stil")

    parser = STILParser(stil_file)
    parser.parse_syntax()
    assert parser.err_line == 23
    assert parser.err_col == 6

def test_syn_err_spec_block_4():
    stil_file = get_stil_file("syn_err_spec_block_4.stil")

    parser = STILParser(stil_file)
    parser.parse_syntax()
    assert parser.err_line == 24    
    assert parser.err_col == 12

def test_syn_err_spec_block_5():
    stil_file = get_stil_file("syn_err_spec_block_5.stil")

    parser = STILParser(stil_file)
    parser.parse_syntax()
    assert parser.err_line == 24    
    assert parser.err_col == 12

def test_syn_err_spec_block_6():
    stil_file = get_stil_file("syn_err_spec_block_6.stil")

    parser = STILParser(stil_file)
    parser.parse_syntax()
    assert parser.err_line == 24    
    assert parser.err_col == 16

def test_syn_err_spec_block_7():
    stil_file = get_stil_file("syn_err_spec_block_7.stil")

    parser = STILParser(stil_file)
    parser.parse_syntax()
    assert parser.err_line == 24    
    assert parser.err_col == 16

def test_syn_err_spec_block_8():
    stil_file = get_stil_file("syn_err_spec_block_8.stil")

    parser = STILParser(stil_file)
    parser.parse_syntax()
    assert parser.err_line == 25
    assert parser.err_col == 1

def test_syn_err_spec_block_9():
    stil_file = get_stil_file("syn_err_spec_block_9.stil")

    parser = STILParser(stil_file)
    parser.parse_syntax()
    assert parser.err_line == 25
    assert parser.err_col == 1

def test_syn_err_spec_block_10():
    stil_file = get_stil_file("syn_err_spec_block_10.stil")

    parser = STILParser(stil_file)
    parser.parse_syntax()
    assert parser.err_line == 25
    assert parser.err_col == 11

def test_syn_err_spec_block_11():
    stil_file = get_stil_file("syn_err_spec_block_11.stil")

    parser = STILParser(stil_file)
    parser.parse_syntax()
    assert parser.err_line == 25
    assert parser.err_col == 11

def test_syn_err_spec_block_12():
    stil_file = get_stil_file("syn_err_spec_block_12.stil")

    parser = STILParser(stil_file)
    parser.parse_syntax()
    assert parser.err_line == 25
    assert parser.err_col == 13

def test_syn_err_spec_block_13():
    stil_file = get_stil_file("syn_err_spec_block_13.stil")

    parser = STILParser(stil_file)
    parser.parse_syntax()
    assert parser.err_line == 25
    assert parser.err_col == 13

def test_syn_err_spec_block_14():
    stil_file = get_stil_file("syn_err_spec_block_14.stil")

    parser = STILParser(stil_file)
    parser.parse_syntax()
    assert parser.err_line == 25
    assert parser.err_col == 13

def test_syn_err_spec_block_15():
    stil_file = get_stil_file("syn_err_spec_block_15.stil")

    parser = STILParser(stil_file)
    parser.parse_syntax()
    assert parser.err_line == 25
    assert parser.err_col == 13

def test_syn_err_spec_block_16():
    stil_file = get_stil_file("syn_err_spec_block_16.stil")

    parser = STILParser(stil_file)
    parser.parse_syntax()
    assert parser.err_line == 26
    assert parser.err_col == 3

def test_syn_err_spec_block_17():
    stil_file = get_stil_file("syn_err_spec_block_17.stil")

    parser = STILParser(stil_file)
    parser.parse_syntax()
    assert parser.err_line == 26
    assert parser.err_col == 3

def test_syn_err_spec_block_18():
    stil_file = get_stil_file("syn_err_spec_block_18.stil")

    parser = STILParser(stil_file)
    parser.parse_syntax()
    assert parser.err_line == 25
    assert parser.err_col == 15

def test_syn_err_spec_block_19():
    stil_file = get_stil_file("syn_err_spec_block_19.stil")

    parser = STILParser(stil_file)
    parser.parse_syntax()
    assert parser.err_line == 25
    assert parser.err_col == 16

def test_syn_err_spec_block_20():
    stil_file = get_stil_file("syn_err_spec_block_20.stil")

    parser = STILParser(stil_file)
    parser.parse_syntax()
    assert parser.err_line == 25
    assert parser.err_col == 47

def test_syn_err_spec_block_21():
    stil_file = get_stil_file("syn_err_spec_block_21.stil")

    parser = STILParser(stil_file)
    parser.parse_syntax()
    assert parser.err_line == 25
    assert parser.err_col == 47

def test_syn_ok_spec_block_1():
    stil_file = get_stil_file("syn_ok_spec_block_1.stil")

    parser = STILParser(stil_file)
    parser.parse_syntax()
    assert parser.err_line == -1    
    assert parser.err_col == -1

def test_syn_ok_spec_block_2():
    stil_file = get_stil_file("syn_ok_spec_block_2.stil")

    parser = STILParser(stil_file)
    parser.parse_syntax()
    assert parser.err_line == -1    
    assert parser.err_col == -1

def test_syn_ok_spec_block_3():
    stil_file = get_stil_file("syn_ok_spec_block_3.stil")

    parser = STILParser(stil_file)
    parser.parse_syntax()
    assert parser.err_line == -1    
    assert parser.err_col == -1

def test_issue_55():

    stil_file = get_stil_file("test_issue_55.stil")

    parser = STILParser(stil_file)
    parser.parse_syntax()
    parser.parse_semantic()
    assert parser.err_line == -1
    assert parser.err_col == -1

def test_issue_60():

    stil_file = get_stil_file("test_issue_60.stil")

    parser = STILParser(stil_file)
    parser.parse_syntax()
    parser.parse_semantic()
    assert parser.err_line == -1
    assert parser.err_col == -1
