# -*- coding: utf-8 -*-
import inspect


class ProceduresBlockParser:
    def __init__(self, debug=True):
        self.debug = debug
        # dict key   is the procesures domain name
        # dict value is a list with all procesures defined for this domain
        self.proc_domain2proc_names = {}
        self.last_proc_domain = "*global*"

    def trace(self, func_name, t):
        head = f"{__name__}:{func_name}"

        if isinstance(t, list):
            print(f"{head} rule value {t}")
        else:
            print(f'{head} token value "{t}" at line {t.line} column {t.column}')

    def b_procedures__PROCEDURES_DOMAIN_NAME(self, t):
        if self.debug:
            func_name = inspect.stack()[0][3]
            self.trace(func_name, t)
        self.last_proc_domain = t.value

    def b_procedures__OPEN_PROCEDURES_BLOCK(self, t):
        if self.debug:
            func_name = inspect.stack()[0][3]
            self.trace(func_name, t)

    def b_procedures__PROCEDURE_NAME(self, t):
        if self.debug:
            func_name = inspect.stack()[0][3]
            self.trace(func_name, t)
        proc_names = self.proc_domain2proc_names.get(self.last_proc_domain)
        if proc_names == None:
            proc_names = [t.value]
            self.proc_domain2proc_names[self.last_proc_domain] = proc_names
        else:
            proc_names.append(t.value)

    def b_procedures__open_proc(self, t):
        if self.debug:
            func_name = inspect.stack()[0][3]
            self.trace(func_name, t)

    def b_procedures__pattern_statements__KEYWORD_V(self, t):
        if self.debug:
            func_name = inspect.stack()[0][3]
            self.trace(func_name, t)

    def b_procedures__pattern_statements__KEYWORD_VECTOR(self, t):
        if self.debug:
            func_name = inspect.stack()[0][3]
            self.trace(func_name, t)

    def b_procedures__pattern_statements__SIGREF_EXPR(self, t):
        if self.debug:
            func_name = inspect.stack()[0][3]
            self.trace(func_name, t)

    def b_procedures__pattern_statements__VEC_DATA_STRING(self, t):
        if self.debug:
            func_name = inspect.stack()[0][3]
            self.trace(func_name, t)

    def b_procedures__close_proc(self, t):
        if self.debug:
            func_name = inspect.stack()[0][3]
            self.trace(func_name, t)

    def b_procedures__CLOSE_PROCEDURES_BLOCK(self, t):
        if self.debug:
            func_name = inspect.stack()[0][3]
            self.trace(func_name, t)
            for key in self.proc_domain2proc_names.keys():
                proc_names = self.proc_domain2proc_names.get(key)
                for name in proc_names:
                    print(f" procedure domain {key} -> procedure name {name}")
        self.last_proc_domain = "*global*"
