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
    return os.path.join(str(folder), "stil_files", "va_calc", file_name)


def test_sem_err_signal_groups_block_1():

    fn = "sem_ok_va_calc.stil"
    stil_file = get_stil_file(fn)
    
    out_folder = "compliler_output_"+fn

    compiler = STILDumpCompiler(
        stil_file, expanding_procs=True, is_scan_mem_available=True, out_folder = out_folder
    )
    compiler.compile()
    compiler.calculate_test_cycles()
    assert compiler.err_line == -1
    assert compiler.err_col == -1



def test_multi_pattern_block():

    fn = "multi_pattern_block.stil"
    stil_file = get_stil_file(fn)
    
    out_folder = "compliler_output_"+fn

    compiler = STILDumpCompiler(
        stil_file, expanding_procs=True, is_scan_mem_available=True, out_folder = out_folder
    )
    compiler.compile()
    compiler.calculate_test_cycles()
    assert compiler.err_line == -1
    assert compiler.err_col == -1

