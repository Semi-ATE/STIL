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
    return os.path.join(str(folder), "stil_files", "pattern_exec_block", file_name)


def test_syn_err_pattern_exec_block_1():
    stil_file = get_stil_file("syn_err_pattern_exec_block_1.stil")

    parser = STILParser(stil_file)
    parser.parse_syntax()
    assert parser.err_line == 40
    assert parser.err_col == 12


def test_sem_err_pattern_exec_block_1():
    stil_file = get_stil_file("sem_err_pattern_exec_block_1.stil")

    parser = STILParser(stil_file)
    parser.parse_syntax()
    parser.parse_semantic()
    assert parser.err_line == 44
    assert parser.err_col == 13

