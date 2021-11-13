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
    return os.path.join(str(folder), "stil_files", "signals_block", file_name)

def test_syn_err_signals_block_1():
  
    stil_file = get_stil_file("syn_err_signals_block_1.stil")

    parser = STILParser(stil_file)
    parser.parse_syntax()
    assert parser.err_line == 3
    assert parser.err_col == 9

def test_syn_err_signals_block_2():
  
    stil_file = get_stil_file("syn_err_signals_block_2.stil")

    parser = STILParser(stil_file)
    parser.parse_syntax()
    assert parser.err_line == 3
    assert parser.err_col == 9

def test_syn_err_signals_block_3():

    stil_file = get_stil_file("syn_err_signals_block_3.stil")

    parser = STILParser(stil_file)
    parser.parse_syntax()
    assert parser.err_line == 4
    assert parser.err_col == 12

def test_syn_err_signals_block_4():
  
    stil_file = get_stil_file("syn_err_signals_block_4.stil")

    parser = STILParser(stil_file)
    parser.parse_syntax()
    assert parser.err_line == 4
    assert parser.err_col == 12

def test_syn_err_signals_block_5():
  
    stil_file = get_stil_file("syn_err_signals_block_5.stil")

    parser = STILParser(stil_file)
    parser.parse_syntax()
    assert parser.err_line == 4
    assert parser.err_col == 15

def test_syn_err_signals_block_6():
  
    stil_file = get_stil_file("syn_err_signals_block_6.stil")

    parser = STILParser(stil_file)
    parser.parse_syntax()
    assert parser.err_line == 4
    assert parser.err_col == 17

def test_syn_err_signals_block_7():
  
    stil_file = get_stil_file("syn_err_signals_block_7.stil")

    parser = STILParser(stil_file)
    parser.parse_syntax()
    assert parser.err_line == 4
    assert parser.err_col == 29

def test_syn_err_signals_block_8():
  
    stil_file = get_stil_file("syn_err_signals_block_8.stil")

    parser = STILParser(stil_file)
    parser.parse_syntax()
    assert parser.err_line == 4
    assert parser.err_col == 30

def test_syn_err_signals_block_9():
  
    stil_file = get_stil_file("syn_err_signals_block_9.stil")

    parser = STILParser(stil_file)
    parser.parse_syntax()
    assert parser.err_line == 4
    assert parser.err_col == 22

def test_syn_err_signals_block_10():
  
    stil_file = get_stil_file("syn_err_signals_block_10.stil")

    parser = STILParser(stil_file)
    parser.parse_syntax()
    assert parser.err_line == 4
    assert parser.err_col == 25

def test_syn_err_signals_block_11():
  
    stil_file = get_stil_file("syn_err_signals_block_11.stil")

    parser = STILParser(stil_file)
    parser.parse_syntax()
    assert parser.err_line == 4
    assert parser.err_col == 27

def test_syn_err_signals_block_12():
  
    stil_file = get_stil_file("syn_err_signals_block_12.stil")

    parser = STILParser(stil_file)
    parser.parse_syntax()
    assert parser.err_line == 4
    assert parser.err_col == 24

def test_syn_err_signals_block_13():
  
    stil_file = get_stil_file("syn_err_signals_block_13.stil")

    parser = STILParser(stil_file)
    parser.parse_syntax()
    assert parser.err_line == 4
    assert parser.err_col == 25

def test_syn_err_signals_block_14():
  
    stil_file = get_stil_file("syn_err_signals_block_14.stil")

    parser = STILParser(stil_file)
    parser.parse_syntax()
    assert parser.err_line == 4
    assert parser.err_col == 30

def test_syn_err_signals_block_15():
  
    stil_file = get_stil_file("syn_err_signals_block_15.stil")

    parser = STILParser(stil_file)
    parser.parse_syntax()
    assert parser.err_line == 4
    assert parser.err_col == 34

def test_syn_ok_signals_block_1():
  
    stil_file = get_stil_file("syn_ok_signals_block_1.stil")

    parser = STILParser(stil_file)
    parser.parse_syntax()
    assert parser.err_line == -1
    assert parser.err_col == -1

def test_sem_err_signals_block_1():
  
    stil_file = get_stil_file("sem_err_signals_block_1.stil")

    parser = STILParser(stil_file)
    parser.parse_syntax()
    parser.parse_semantic()
    assert parser.err_line == 19
    assert parser.err_col == 5

def test_sem_ok_signals_block_1():

    stil_file = get_stil_file("sem_ok_signals_block_1.stil")

    parser = STILParser(stil_file)
    parser.parse_syntax()
    parser.parse_semantic()
    assert parser.err_line == -1
    assert parser.err_col == -1


