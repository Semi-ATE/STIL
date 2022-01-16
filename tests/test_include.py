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
    return os.path.join(str(folder), "stil_files", "include", file_name)


def test_syn_err_include_1():
    stil_file = get_stil_file("syn_err_include_1.stil")

    parser = STILParser(stil_file)
    parser.parse_syntax(preprocess_include = False)
    assert parser.err_line == 3
    assert parser.err_col == 1

def test_syn_err_include_2():
    stil_file = get_stil_file("syn_err_include_2.stil")

    parser = STILParser(stil_file)
    parser.parse_syntax(preprocess_include = False)
    assert parser.err_line == 3
    assert parser.err_col == 9

def test_syn_err_include_3():
    stil_file = get_stil_file("syn_err_include_3.stil")

    parser = STILParser(stil_file)
    parser.parse_syntax(preprocess_include = False)
    assert parser.err_line == 3
    assert parser.err_col == 9

def test_syn_err_include_4():
    stil_file = get_stil_file("syn_err_include_4.stil")

    parser = STILParser(stil_file)
    parser.parse_syntax(preprocess_include = False)
    assert parser.err_line == 3
    assert parser.err_col == 24

def test_syn_err_include_5():
    stil_file = get_stil_file("syn_err_include_5.stil")

    parser = STILParser(stil_file)
    parser.parse_syntax(preprocess_include = False)
    assert parser.err_line == 3
    assert parser.err_col == 31

def test_syn_err_include_6():
    stil_file = get_stil_file("syn_err_include_6.stil")

    parser = STILParser(stil_file)
    parser.parse_syntax()
    assert parser.err_line == 6
    assert parser.err_col == 10

    inc_stil_file = stil_file + ".wo_include"
    if os.path.exists(inc_stil_file):
        os.remove(inc_stil_file)

def test_syn_ok_include_1():
    stil_file = get_stil_file("syn_ok_include_1.stil")

    parser = STILParser(stil_file)
    parser.parse_syntax(preprocess_include = False)
    assert parser.err_line == -1
    assert parser.err_col == -1

def test_syn_ok_include_2():
    stil_file = get_stil_file("syn_ok_include_2.stil")

    parser = STILParser(stil_file)
    parser.parse_syntax(preprocess_include = False)
    assert parser.err_line == -1
    assert parser.err_col == -1

def test_syn_ok_include_3():
    stil_file = get_stil_file("syn_ok_include_3.stil")

    parser = STILParser(stil_file)
    parser.parse_syntax(preprocess_include = False)
    assert parser.err_line == -1
    assert parser.err_col == -1


def test_syn_ok_include_4():
    stil_file = get_stil_file("syn_ok_include_4.stil")

    parser = STILParser(stil_file)
    parser.parse_syntax()
    assert parser.err_line == -1
    assert parser.err_col == -1
    
    inc_stil_file = stil_file + ".wo_include"
    if os.path.exists(inc_stil_file):
        os.remove(inc_stil_file)


