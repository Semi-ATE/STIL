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
    return os.path.join(str(folder), "stil_files", "pattern_burst_block", file_name)


def test_syn_err_pattern_burst_block_1():
    stil_file = get_stil_file("syn_err_pattern_burst_block_1.stil")

    parser = STILParser(stil_file)
    parser.parse_syntax()
    assert parser.err_line == 36
    assert parser.err_col == 14

def test_syn_err_pattern_burst_block_2():
    stil_file = get_stil_file("syn_err_pattern_burst_block_2.stil")

    parser = STILParser(stil_file)
    parser.parse_syntax()
    assert parser.err_line == 36
    assert parser.err_col == 19

def test_syn_err_pattern_burst_block_3():
    stil_file = get_stil_file("syn_err_pattern_burst_block_3.stil")

    parser = STILParser(stil_file)
    parser.parse_syntax()
    assert parser.err_line == 36
    assert parser.err_col == 14

def test_syn_err_pattern_burst_block_4():
    stil_file = get_stil_file("syn_err_pattern_burst_block_4.stil")

    parser = STILParser(stil_file)
    parser.parse_syntax()
    assert parser.err_line == 37
    assert parser.err_col == 3

def test_syn_err_pattern_burst_block_5():
    stil_file = get_stil_file("syn_err_pattern_burst_block_5.stil")

    parser = STILParser(stil_file)
    parser.parse_syntax()
    assert parser.err_line == 37
    assert parser.err_col == 15

def test_syn_err_pattern_burst_block_6():
    stil_file = get_stil_file("syn_err_pattern_burst_block_6.stil")

    parser = STILParser(stil_file)
    parser.parse_syntax()
    assert parser.err_line == 37
    assert parser.err_col == 12

def test_syn_err_pattern_burst_block_7():
    stil_file = get_stil_file("syn_err_pattern_burst_block_7.stil")

    parser = STILParser(stil_file)
    parser.parse_syntax()
    assert parser.err_line == 37
    assert parser.err_col == 13

def test_syn_err_pattern_burst_block_8():
    stil_file = get_stil_file("syn_err_pattern_burst_block_8.stil")

    parser = STILParser(stil_file)
    parser.parse_syntax()
    assert parser.err_line == 37
    assert parser.err_col == 17

def test_syn_err_pattern_burst_block_9():
    stil_file = get_stil_file("syn_err_pattern_burst_block_9.stil")

    parser = STILParser(stil_file)
    parser.parse_syntax()
    assert parser.err_line == 37
    assert parser.err_col == 8

def test_syn_err_pattern_burst_block_10():
    stil_file = get_stil_file("syn_err_pattern_burst_block_10.stil")

    parser = STILParser(stil_file)
    parser.parse_syntax()
    assert parser.err_line == 37
    assert parser.err_col == 7

def test_syn_err_pattern_burst_block_11():
    stil_file = get_stil_file("syn_err_pattern_burst_block_11.stil")

    parser = STILParser(stil_file)
    parser.parse_syntax()
    assert parser.err_line == 37
    assert parser.err_col == 14

# TODO Fix the syntax parser
#def test_syn_err_pattern_burst_block_12():
#    stil_file = get_stil_file("syn_err_pattern_burst_block_12.stil")
#
#    parser = STILParser(stil_file)
#    parser.parse_syntax()
#    assert parser.err_line == 37
#    assert parser.err_col == 21

def test_syn_err_pattern_burst_block_13():
    stil_file = get_stil_file("syn_err_pattern_burst_block_13.stil")

    parser = STILParser(stil_file)
    parser.parse_syntax()
    assert parser.err_line == 37
    assert parser.err_col == 33

def test_syn_err_pattern_burst_block_14():
    stil_file = get_stil_file("syn_err_pattern_burst_block_14.stil")

    parser = STILParser(stil_file)
    parser.parse_syntax()
    assert parser.err_line == 37
    assert parser.err_col == 10

def test_syn_err_pattern_burst_block_15():
    stil_file = get_stil_file("syn_err_pattern_burst_block_15.stil")

    parser = STILParser(stil_file)
    parser.parse_syntax()
    assert parser.err_line == 37
    assert parser.err_col == 25

def test_syn_err_pattern_burst_block_16():
    stil_file = get_stil_file("syn_err_pattern_burst_block_16.stil")

    parser = STILParser(stil_file)
    parser.parse_syntax()
    assert parser.err_line == 37
    assert parser.err_col == 27

def test_syn_err_pattern_burst_block_17():
    stil_file = get_stil_file("syn_err_pattern_burst_block_17.stil")

    parser = STILParser(stil_file)
    parser.parse_syntax()
    assert parser.err_line == 38
    assert parser.err_col == 1

def test_syn_ok_pattern_burst_block_1():
    stil_file = get_stil_file("syn_ok_pattern_burst_block_1.stil")

    parser = STILParser(stil_file)
    parser.parse_syntax()
    assert parser.err_line == -1
    assert parser.err_col == -1

def test_syn_ok_pattern_burst_block_2():
    stil_file = get_stil_file("syn_ok_pattern_burst_block_2.stil")

    parser = STILParser(stil_file)
    parser.parse_syntax()
    assert parser.err_line == -1
    assert parser.err_col == -1

def test_syn_ok_pattern_burst_block_3():
    stil_file = get_stil_file("syn_ok_pattern_burst_block_3.stil")

    parser = STILParser(stil_file)
    parser.parse_syntax()
    assert parser.err_line == -1
    assert parser.err_col == -1

def test_syn_ok_pattern_burst_block_4():
    stil_file = get_stil_file("syn_ok_pattern_burst_block_4.stil")

    parser = STILParser(stil_file)
    parser.parse_syntax()
    assert parser.err_line == -1
    assert parser.err_col == -1

def test_sem_err_pattern_burst_block_1():
    stil_file = get_stil_file("sem_err_pattern_burst_block_1.stil")

    parser = STILParser(stil_file)
    parser.parse_syntax()
    parser.parse_semantic()
    assert parser.err_line == 37
    assert parser.err_col == 16

def test_sem_err_pattern_burst_block_2():
    stil_file = get_stil_file("sem_err_pattern_burst_block_2.stil")

    parser = STILParser(stil_file)
    parser.parse_syntax()
    parser.parse_semantic()
    assert parser.err_line == 55
    assert parser.err_col == 11

def test_sem_err_pattern_burst_block_3():
    stil_file = get_stil_file("sem_err_pattern_burst_block_3.stil")

    parser = STILParser(stil_file)
    parser.parse_syntax()
    parser.parse_semantic()
    assert parser.err_line == 55
    assert parser.err_col == 10

def test_sem_err_pattern_burst_block_4():
    stil_file = get_stil_file("sem_err_pattern_burst_block_4.stil")

    parser = STILParser(stil_file)
    parser.parse_syntax()
    parser.parse_semantic()
    assert parser.err_line == 37
    assert parser.err_col == 13



