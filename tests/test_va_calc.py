# -*- coding: utf-8 -*-

import os
import sys

try:
    from Semi_ATE.STIL.parsers.STILDumpCompiler import STILDumpCompiler
    from Semi_ATE.STIL.lsp.VACounter import VACounter
except:
    cwd = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.insert(0, cwd)
    from Semi_ATE.STIL.lsp.VACounter import VACounter
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

    fn = "multi_pattern_block3.stil"
    stil_file = get_stil_file(fn)
    
    out_folder = "compliler_output_"+fn

    compiler = STILDumpCompiler(
        stil_file, expanding_procs=True, is_scan_mem_available=True, out_folder = out_folder
    )
    compiler.compile()
    compiler.calculate_test_cycles()
    assert compiler.err_line == -1
    assert compiler.err_col == -1

def test_va_calc_no_macro_proc():
    fn = "multi_pattern_block3.stil"
    stil_file = get_stil_file(fn)
    vac = VACounter(stil_file)
    vac.analise()
    result = vac.eof()
    assert result == {'patt1': [(7, 60), (8, 61)], 'patt2': [(3, 66), (4, 67), (5, 68), (6, 69)], 'patt3': [(0, 74), (1, 75), (2, 76)]}
    
def test_va_calc_with_macro_proc_simple():
    fn = "multi_pattern_block.stil"
    stil_file = get_stil_file(fn)
    vac = VACounter(stil_file)
    vac.analise()
    result = vac.eof()
    assert result == {'patt1': [(13, 60), (17, 62)], 'patt2': [(3, 67), (7, 69), (8, 70), (12, 72)], 'patt3': [(0, 77), (1, 78), (2, 79)]}

def test_va_calc_with_macro_proc_multiple():
    fn = "multi_pattern_block2.stil"
    stil_file = get_stil_file(fn)
    vac = VACounter(stil_file)
    vac.analise()
    result = vac.eof()
    assert result == {'patt1': [(10, 60), (14, 62)], 'patt2': [(3, 67), (4, 68), (5, 69), (9, 71)], 'patt3': [(0, 76), (1, 77), (2, 78)]}


