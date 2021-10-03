# -*- coding: utf-8 -*-
class STILSemanticException(Exception):
    def __init__(self, err_line, err_col, err_msg):
        print(f"new STILSemanticException {err_line} {err_col} {err_msg}")
        self.line = err_line 
        self.col  = err_col 
        self.msg  = err_msg 
