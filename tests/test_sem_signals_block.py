# -*- coding: utf-8 -*-

import os
from Semi_ATE.STIL.parsers.STILParser import STILParser

def get_stil_file(file_name):
    folder = os.path.dirname(__file__)
    return os.path.join(str(folder), "stil_files", "signals_block", file_name)

def test_sem_err_signals_block_1():

  
    stil_file = get_stil_file("sem_err_signals_block_1.stil")

    parser = STILParser()
    tree = parser.parse_syntax(stil_file)
    parser.parse_semantic(tree, stil_file, debug = False)
    assert parser.err_line == 19
    assert parser.err_col == 5
