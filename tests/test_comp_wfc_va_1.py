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
    return os.path.join(str(folder), "stil_files", "compiler", file_name)


def test_sem_err_signal_groups_block_1():

    stil_file = get_stil_file("test_diff_siggroup.stil")

    compiler = STILDumpCompiler(
        stil_file, expanding_procs=False, is_scan_mem_available=True, out_folder="compiler_test_diff_siggroup.stil"
    )
    compiler.compile()
