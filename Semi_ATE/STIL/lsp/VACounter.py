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

s1 = time.time()

class VACounter(STILParser):
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
        self.va_count = 0
        self.patt_exec_order = []
        self.patt_va_list = {}
        self.macro2va = {}
        self.proc_calls = {}
        self.macro_calls = {}

    def b_pattern_exec__open_pattern_exec_block(self, t):
        super().b_pattern_exec__open_pattern_exec_block(t)
        if self.debug:  print("STIL.lsp.VACount Open PE")
        self.patt_exec_order.append(self.curr_patt_exec)  
        self.va_count = 0  
#########################################################################168
    def b_pattern__pattern_statements__CALL_PROC_NAME(self, t):
        super().b_pattern__pattern_statements__CALL_PROC_NAME(t)
        self.proc_calls[self.curr_pattern] = (t.value, t.line)
        if self.debug:  print(f"STIL.lsp.VACount CALL_PROC_NAME:{self.proc_calls}")

    def b_pattern__pattern_statements__CALL_MACRO_NAME(self, t):
        super().b_pattern__pattern_statements__CALL_MACRO_NAME(t)
        self.macro_calls[self.curr_pattern] = (t.value, t.line)
        if self.debug:  print(f"STIL.lsp.VACount CALL_MACRO_NAME:{self.macro_calls}")

##########################################################################
    def b_pattern__pattern_statements__KEYWORD_VECTOR(self, t):
        super().b_pattern__pattern_statements__KEYWORD_VECTOR(t)
        if self.debug:  print(f"STIL.lsp.VACount KEYWORD_VECTOR VACounter:{self.va_count}, Line:{t.line}")
        if self.curr_pattern in self.patt_va_list:
            v = self.patt_va_list[self.curr_pattern]
            v.append((self.va_count, t.line))
        else:
            v = [(self.va_count, t.line)]    
        self.patt_va_list[self.curr_pattern] = v
        self.va_count += 1


    def b_pattern__pattern_statements__KEYWORD_V(self, t):
        super().b_pattern__pattern_statements__KEYWORD_V(t)
        if self.debug:  print(f"STIL.lsp.VACount KEYWORD_V VACounter:{self.va_count}, Line:{t.line}")
        if self.curr_pattern in self.patt_va_list:
            v = self.patt_va_list[self.curr_pattern]
            v.append((self.va_count, t.line))
        else:
            v = [(self.va_count, t.line)]    
        self.patt_va_list[self.curr_pattern] = v
        self.va_count += 1

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
        # at the end of the file:
        if self.enable_trace:
            if self.debug:  print("Dump compilation is in progress...")
        try:
            vc = 0

            #print(f"Pattern exec list type:{type(self.patt_exec_block2patt_burst.keys())}")
            for pattern_exec_block in self.patt_exec_order:

                patt_bursts = self.patt_exec_block2patt_burst[pattern_exec_block]
                #For every pattern burst block in the pattern exec block
                #print(f"Pattern burst list type:{type(patt_bursts)}")
                for patt_burst in patt_bursts:
                    macro_dom_name = self.patt_burst2macro_domain[patt_burst]#domain names for current burst
                    proc_dom_name = self.patt_burst2proc_domain[patt_burst]

                    pattern_list = self.patt_burst_block2pattern_blocks[patt_burst]
                    passed_va = 0
                    non_countable_vas = 0
                    # For every pattern block in the pattern burst block
                    #print(f"Pattern block list type:{type(pattern_list)}")
                    for patt in pattern_list:
                        call2va = {}
                        passed_calls = []
                        passed_macros = []

                        if bool(self.patt2call[patt]):
                            for call in self.patt2call[patt]:
                                call_proc = str(proc_dom_name) + "::" + str(call)
                                call2va[call] = self.proc2va[call_proc]

                        if bool(self.patt2macro[patt]): 
                            for macro in self.patt2macro[patt]:
                                macro_macro = str(macro_dom_name) + "::" + str(macro)
                                call2va[macro] = self.macro2va[macro_macro] 

                        for v in range(len(self.patt_va_list[patt])):
                            lst = list(self.patt_va_list[patt][v])
                            lst[0] = passed_va
                            
                            for call in self.proc_calls:
                                if patt == call and lst[1] > self.proc_calls[call][1] and self.proc_calls[call][0] not in passed_calls:
                                    non_countable_vas += call2va[self.proc_calls[call][0]]
                                    passed_calls.append(self.proc_calls[call][0])

                            for call in self.macro_calls:
                                if patt == call and lst[1] > self.macro_calls[call][1] and self.macro_calls[call][0] not in passed_macros:
                                    non_countable_vas += call2va[self.macro_calls[call][0]]
                                    passed_macros.append(self.macro_calls[call][0])

                            lst[0]+=non_countable_vas        
                            self.patt_va_list[patt][v] = tuple(lst)
                            passed_va += 1
                            

            if self.debug:  print(f"STIL.lsp.VACount Pattern VA List: {self.patt_va_list}")
            if self.debug:  print(f"STIL.lsp.VACount time:{time.time()-s1}")

        except STILDumpCompilerException as e:
            print(e.msg)
            os._exit(1)

        return self.patt_va_list    

def main():
    test = VACounter("../../../tests/stil_files/va_calc/multi_pattern_block.stil", debug=True)
    test.analise()
    
if __name__ == "__main__":
    main()
