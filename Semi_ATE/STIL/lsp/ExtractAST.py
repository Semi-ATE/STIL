import sys
import os
import argparse
import time
import inspect
import time
import lark
import itertools
from collections import OrderedDict
sys.path.append(os.path.join(os.path.dirname(__file__),'../../'))

from VACounter import VACounter

from STIL.parsers.STILParser import STILParser

from STIL.parsers.WFCUtils import WFCUtils
from STIL.parsers.DomainUtils import DomainUtils
from STIL.parsers.PattVecCmd import PattVecCmd
from STIL.parsers.HashInfo import HashInfo
from STIL.parsers.STILDumpCompilerExceptions import STILDumpCompilerException      

s1 = time.time()

class ExtractAST(STILParser):
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
        self.last = None
        self.clean = True
        self.open_brackets = []
        self.strpat = ["b_timing__",
        "b_pattern__pattern_statements__",
        "b_signals__",
        "b_signal_groups__",
        "b_pattern_burst__",
        "b_macrodefs__",
        "b_procedures__",
        "b_pattern__",
        "b_pattern_exec__",
        "pattern_statements__",
        "b_pattern__pattern_statements__",
        "b_procedures__pattern_statements__",
        "b_macrodefs__pattern_statements__"]
        self.vas = []

    def analise(self):
        if self.enable_trace:
            if self.debug:  print("\nSyntax parsing is in progress...")
        self.parse_syntax()
        if self.err_line != -1:
            print(f"Error on line {self.err_line}, column {self.err_col}")
            print(self.err_msg)
        #print(self.tree.pretty())    

    def eof(self):
        # at the end of the file:
        if self.enable_trace:
            if self.debug:  print("Dump compilation is in progress...")

        try:
            vac = VACounter(self.stil_file)
            vac.analise()
            self.vas = vac.eof()##Get VAs
            self.change_helper(self.tree.children)
            print(self.tree.pretty())    

        except STILDumpCompilerException as e:
            print(e.msg)
            os._exit(1)    

    def change_helper(self, ast):
        if not isinstance(ast, list):
            return     
        for t in ast:
            if hasattr(t, 'children'):##Branch
                self.change_token(t)
                ##Add meta data to branch
                self.change_helper(t.children)
                self.last = t
            elif self.last != None:##Leaf
                if not self.clean:
                    ttype = t.type
                ##Remove prefixes    
                else:
                    for strp in self.strpat:
                        if strp in t.type:
                            ttype = t.type.removeprefix(strp)
                
                ##Add vector addresses
                if ttype in ["KEYWORD_V", "KEYWORD_VECTOR"]:
                    for patt in self.vas:
                        for vector in self.vas[patt]:
                            if vector[1] == t.line:
                                ttype += f" VA:{vector[0]},"

                ##Add meta data to leaf             
                self.last.children.append(f"{ttype} Line:{t.line}, Column:{t.column}")
                
    def change_token(self, token):
        if hasattr(token, "data"):
            ln = token.line
            cl = token.column
            if "open" in token.data:
                self.open_brackets.append(token)
            if "close" in token.data:
                if len(self.open_brackets) > 0:
                    self.open_brackets[-1].data += f", End line:{ln}"
                    self.open_brackets[-1].end_line = ln
                    self.open_brackets.pop(-1)

            if not self.clean:
                token.data += f" Line:{ln}, Column:{cl}"
            else:
                token.data += f" Line:{ln}, Column:{cl}"
                for strp in self.strpat:
                    if strp in token.data:
                        token.data = token.data.removeprefix(strp)
                  
def main():
    test = ExtractAST("../../../tests/stil_files/va_calc/multi_pattern_block.stil", debug=True)
    test.analise()
    test.eof()
    
if __name__ == "__main__":
    main()
