# -*- coding: utf-8 -*-
import inspect


class MacroDefsBlockParser:
    def __init__(self, debug=True):
        self.debug = debug
        # dict key   is the macrodefs domain name
        # dict value is a list with all macros defined for this domain
        self.macro_domain2macro_names = {}
        self.last_macro_domain = "*global*"

    def trace(self, func_name, t):
        head = f"{__name__}:{func_name}"

        if isinstance(t, list):
            print(f"{head} rule value {t}")
        else:
            print(f'{head} token value "{t}" at line {t.line} column {t.column}')

    def b_macrodefs__MACRODEFS_DOMAIN_NAME(self, t):
        if self.debug:
            func_name = inspect.stack()[0][3]
            self.trace(func_name, t)
        self.last_macro_domain = t.value

    def b_macrodefs__OPEN_MACRO_DEFS_BLOCK(self, t):
        if self.debug:
            func_name = inspect.stack()[0][3]
            self.trace(func_name, t)

    def b_macrodefs__MACRO_NAME(self, t):
        if self.debug:
            func_name = inspect.stack()[0][3]
            self.trace(func_name, t)
        macro_names = self.macro_domain2macro_names.get(self.last_macro_domain)
        if macro_names == None:
            macro_names = [t.value]
            self.macro_domain2macro_names[self.last_macro_domain] = macro_names
        else:
            macro_names.append(t.value)

    def b_macrodefs__open_macro(self, t):
        if self.debug:
            func_name = inspect.stack()[0][3]
            self.trace(func_name, t)

    def b_macrodefs__pattern_statements__KEYWORD_V(self, t):
        if self.debug:
            func_name = inspect.stack()[0][3]
            self.trace(func_name, t)

    def b_macrodefs__pattern_statements__KEYWORD_VECTOR(self, t):
        if self.debug:
            func_name = inspect.stack()[0][3]
            self.trace(func_name, t)

    def b_macrodefs__pattern_statements__SIGREF_EXPR(self, t):
        if self.debug:
            func_name = inspect.stack()[0][3]
            self.trace(func_name, t)

    def b_macrodefs__pattern_statements__VEC_DATA_STRING(self, t):
        if self.debug:
            func_name = inspect.stack()[0][3]
            self.trace(func_name, t)

    def b_macrodefs__close_macro(self, t):
        if self.debug:
            func_name = inspect.stack()[0][3]
            self.trace(func_name, t)

    def b_macrodefs__CLOSE_MACRO_DEFS_BLOCK(self, t):
        if self.debug:
            func_name = inspect.stack()[0][3]
            self.trace(func_name, t)
            for key in self.macro_domain2macro_names.keys():
                macro_names = self.macro_domain2macro_names.get(key)
                for name in macro_names:
                    print(f" macro domain {key} -> macro name {name}")
        self.last_macro_domain = "*global*"
