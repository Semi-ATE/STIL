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
    return os.path.join(str(folder), "stil_files", "user_keywords", file_name)

def test_sem_err_user_keyword_1():

    stil_file = get_stil_file("test_sem_err_user_keyword_1.stil")

    parser = STILParser(stil_file)
    parser.parse_syntax()
    parser.parse_semantic()

    assert parser.err_line == 66
    assert parser.err_col == 17

def test_sem_err_user_keyword_2():

    stil_file = get_stil_file("test_sem_err_user_keyword_2.stil")

    parser = STILParser(stil_file)
    parser.parse_syntax()
    parser.parse_semantic()

    assert parser.err_line == 35
    assert parser.err_col == 17

def test_sem_err_user_keyword_3():

    stil_file = get_stil_file("test_sem_err_user_keyword_3.stil")

    parser = STILParser(stil_file)
    parser.parse_syntax()
    parser.parse_semantic()

    assert parser.err_line == 36
    assert parser.err_col == 17
    

def test_sem_ok_user_keyword_1():

    stil_file = get_stil_file("test_sem_ok_user_keyword_1.stil")

    parser = STILParser(stil_file)
    parser.parse_syntax()
    parser.parse_semantic()

    assert parser.err_line == -1
    assert parser.err_col == -1

def test_sem_ok_user_keyword_2():

    stil_file = get_stil_file("test_sem_ok_user_keyword_2.stil")

    parser = STILParser(stil_file)
    parser.parse_syntax()
    parser.parse_semantic()

    assert parser.err_line == -1
    assert parser.err_col == -1

def test_sem_ok_user_keyword_3():

    stil_file = get_stil_file("test_sem_ok_user_keyword_3.stil")

    parser = STILParser(stil_file)
    parser.parse_syntax()
    parser.parse_semantic()

    assert parser.err_line == -1
    assert parser.err_col == -1

def test_sem_ok_user_keyword_4():

    stil_file = get_stil_file("test_sem_ok_user_keyword_4.stil")

    parser = STILParser(stil_file)
    parser.parse_syntax()
    parser.parse_semantic()

    assert parser.err_line == -1
    assert parser.err_col == -1

def test_sem_ok_user_keyword_5():

    stil_file = get_stil_file("test_sem_ok_user_keyword_5.stil")

    parser = STILParser(stil_file)
    parser.parse_syntax()
    parser.parse_semantic()

    assert parser.err_line == -1
    assert parser.err_col == -1
