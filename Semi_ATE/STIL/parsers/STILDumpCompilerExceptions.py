# -*- coding: utf-8 -*-
class STILDumpCompilerInternalException(Exception):
    def __init__(self, err_msg):
        self.msg  = err_msg 

class STILDumpCompilerException(Exception):
    def __init__(self, err_line, err_col, err_msg):
        self.line = err_line 
        self.col  = err_col 
        self.msg  = err_msg 
