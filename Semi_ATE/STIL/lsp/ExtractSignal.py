import sys
import os
import argparse
import time
import inspect
import time
sys.path.append(os.path.join(os.path.dirname(__file__),'../../'))

from STIL.parsers.STILParser import STILParser

from STIL.parsers.WFCUtils import WFCUtils
from STIL.parsers.DomainUtils import DomainUtils
from STIL.parsers.PattVecCmd import PattVecCmd
from STIL.parsers.HashInfo import HashInfo
from STIL.parsers.STILDumpCompilerExceptions import STILDumpCompilerException 

class ExtractSignal(STILParser):
    def __init__(
        self,
        stil_file,
        out_folder = "",
        signals_order_file = None,
        propagate_positions = True,
        expanding_procs = False,
        is_scan_mem_available = False,
        dump_data = True,
        enable_trace = True,
        stil_lark_file = None,
        extra_grammars = [],
        debug = False,
    ):

        STILParser.__init__(self, stil_file, propagate_positions, expanding_procs, stil_lark_file, extra_grammars, debug)

        out_folder = os.path.join(os.getcwd(), out_folder)
        try: 
            os.mkdir(out_folder)
        except OSError: 
            pass

        self.dump_data = dump_data
        self.out_folder = out_folder
        self.enable_trace = enable_trace
        self.signal_tokens = {}


    def b_signals__SIGNAL_NAME(self, t):
    	super().b_signals__SIGNAL_NAME(t)
    	self.signal_tokens[t.value] = t.line

    def b_signals__SIGNAL_TYPE(self, t):
    	super().b_signals__SIGNAL_TYPE(t)
    	for tokens in self.signal_tokens:
    		if self.signal_tokens[tokens] == t.line:
    			self.signal_tokens[tokens] = (t.value, t.line)

    def analise(self):
        if self.enable_trace:
            if self.debug:  print("\nSyntax parsing is in progress...")
        self.parse_syntax()
        if self.enable_trace:
            if self.debug:  print("Semantic analisys is in progress...")
        self.parse_semantic()
        if self.err_line != -1:
        	print(f"Error on line {self.err_line}, column {self.err_col}")
        	print(self.err_msg)


    def eof(self): 
        if self.enable_trace:
            if self.debug:  print("Dump compilation is in progress...")
        try:
            if self.enable_trace: print(self.signal_tokens)
        except STILDumpCompilerException as e:
            print(e.msg)
            os._exit(1)

        return self.signal_tokens   

def main():
    test = ExtractSignal("../../../tests/stil_files/va_calc/multi_pattern_block.stil", debug=False)
    test.analise()
    
if __name__ == "__main__":
    main()
