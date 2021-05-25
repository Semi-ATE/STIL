# -*- coding: utf-8 -*-

import os
from Semi_ATE.STIL.parsers.STILParser import STILParser

def get_stil_file(file_name):
    folder = os.path.dirname(__file__)
    return os.path.join(str(folder), "stil_files", "stil_block", file_name)

    
def test_syn_err_stil_block_1():
    
    stil_file = get_stil_file("syn_err_stil_block_1.stil")

    parser = STILParser()
    tree = parser.parse_syntax(stil_file)
    if tree == None:
        assert parser.err_line == 1
        assert parser.err_col == 1

def test_syn_err_stil_block_2():

    stil_file = get_stil_file("syn_err_stil_block_2.stil")

    parser = STILParser()
    tree = parser.parse_syntax(stil_file)
    if tree == None:
        assert parser.err_line == 1
        assert parser.err_col == 5

def test_syn_err_stil_block_3():

    stil_file = get_stil_file("syn_err_stil_block_3.stil")

    parser = STILParser()
    tree = parser.parse_syntax(stil_file)
    if tree == None:
        assert parser.err_line == 1
        assert parser.err_col == 6

def test_syn_err_stil_block_4():

    stil_file = get_stil_file("syn_err_stil_block_4.stil")

    parser = STILParser()
    tree = parser.parse_syntax(stil_file)
    if tree == None:
        assert parser.err_line == 1
        assert parser.err_col == 6

def test_syn_err_stil_block_5():

    stil_file = get_stil_file("syn_err_stil_block_5.stil")

    parser = STILParser()
    tree = parser.parse_syntax(stil_file)
    if tree == None:
        assert parser.err_line == 1
        assert parser.err_col == 6

def test_syn_err_stil_block_6():

    stil_file = get_stil_file("syn_err_stil_block_6.stil")

    parser = STILParser()
    tree = parser.parse_syntax(stil_file)
    if tree == None:
        assert parser.err_line == 1
        assert parser.err_col == 11

def test_syn_err_stil_block_7():

    stil_file = get_stil_file("syn_err_stil_block_7.stil")

    parser = STILParser()
    tree = parser.parse_syntax(stil_file)
    if tree == None:
        assert parser.err_line == 1
        assert parser.err_col == 12

def test_syn_err_stil_block_8():

    stil_file = get_stil_file("syn_err_stil_block_8.stil")

    parser = STILParser()
    tree = parser.parse_syntax(stil_file)
    if tree == None:
        assert parser.err_line == 1
        assert parser.err_col == 19

def test_syn_err_stil_block_9():

    stil_file = get_stil_file("syn_err_stil_block_9.stil")

    parser = STILParser()
    tree = parser.parse_syntax(stil_file)
    if tree == None:
        assert parser.err_line == 1
        assert parser.err_col == 40

def test_syn_err_stil_block_10():

    stil_file = get_stil_file("syn_err_stil_block_10.stil")

    parser = STILParser()
    tree = parser.parse_syntax(stil_file)
    if tree == None:
        assert parser.err_line == 1
        assert parser.err_col == 39

def test_sem_err_stil_block_1():
    
    stil_file = get_stil_file("sem_err_stil_block_1.stil")

    parser = STILParser()
    tree = parser.parse_syntax(stil_file)
    parser.parse_semantic(tree, stil_file)
