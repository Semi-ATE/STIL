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
    return os.path.join(str(folder), "stil_files", "scan_structures_block", file_name)

def test_issue_51():
    stil_file = get_stil_file("test_issue_51.stil")

    parser = STILParser(stil_file)
    parser.parse_syntax()
    parser.parse_semantic()

    assert parser.err_line == -1
    assert parser.err_col == -1
