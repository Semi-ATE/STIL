# -*- coding: utf-8 -*-

import os
from Semi_ATE.STIL.parsers.STILParser import STILParser

def get_stil_file(file_name):
    folder = os.path.dirname(__file__)
    return os.path.join(str(folder), "stil_files", "header_block", file_name)
        
def test_syn_err_header_block_1():

    stil_file = get_stil_file("syn_err_header_block_1.stil")

    parser = STILParser()
    tree = parser.parse_syntax(stil_file)
    if tree == None:
        assert parser.err_line == 3
        assert parser.err_col == 1
