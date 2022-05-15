# -*- coding: utf-8 -*-
import os
import sys

try:
    from Semi_ATE.STIL.parsers.STILDumpCompiler import STILDumpCompiler
except:
    cwd = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.insert(0, cwd)
    from Semi_ATE.STIL.parsers.STILDumpCompiler import STILDumpCompiler

def get_stil_file(file_name):
    folder = os.path.dirname(__file__)
    return os.path.join(str(folder), "stil_files", file_name)

def test_ok_atpg_1_w_scan():

    stil_file = get_stil_file("test_atpg_1.stil")

    parser = STILDumpCompiler(stil_file, expanding_procs = True, is_scan_mem_available = True, out_folder = "out")
    parser.compile()

    assert parser.err_line == -1
    assert parser.err_col == -1
    
    # ToDo : check the real data

def test_ok_atpg_1_wo_scan():

    stil_file = get_stil_file("test_atpg_1.stil")

    parser = STILDumpCompiler(stil_file, expanding_procs = True, is_scan_mem_available = False, out_folder = "out")
    parser.compile()

    assert parser.err_line == -1
    assert parser.err_col == -1

    # ToDo : check the real data
