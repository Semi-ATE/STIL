# -*- coding: utf-8 -*-

import os
import sys

try:
    from Semi_ATE.STIL.parsers.STILDumpCompiler import STILDumpCompiler
    from Semi_ATE.STIL.lsp.ExtractSignal import ExtractSignal
except:
    cwd = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.insert(0, cwd)
    from Semi_ATE.STIL.lsp.ExtractSignal import ExtractSignal
    from Semi_ATE.STIL.parsers.STILDumpCompiler import STILDumpCompiler


def get_stil_file(file_name):
    folder = os.path.dirname(__file__)
    return os.path.join(str(folder), "stil_files", "va_calc", file_name)

def test_extract_signal():
    fn = "multi_pattern_block.stil"
    stil_file = get_stil_file(fn)
    vac = ExtractSignal(stil_file)
    vac.analise()
    result = vac.eof()
    assert result == {'sig1': ('In', 5), 'sig2': ('Out', 6)}
    