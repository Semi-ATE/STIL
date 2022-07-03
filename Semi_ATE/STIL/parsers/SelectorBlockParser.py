# -*- coding: utf-8 -*-
import inspect
from .DomainUtils import DomainUtils


class SelectorBlockParser:
    def __init__(self, debug=False):
        self.debug = debug

        self.curr_selector = DomainUtils.global_domain
        self.curr_var_name = None
        
        # Key is selector_name::variable_name
        # Value is Min/Typ/Max
        self.selector_var = {}

    def trace(self, func_name, t):
        head = f"{__name__}:{func_name}"

        if isinstance(t, list):
            print(f"{head} rule value {t}")
        else:
            print(f'{head} token value "{t}" at line {t.line} column {t.column}')

    def b_selector__SELECTOR_DOMAIN_NAME(self, t):
        if self.debug:
            func_name = inspect.stack()[0][3]
            self.trace(func_name, t)
            
        self.curr_selector = t.value

    def b_selector__open_selector_block(self, t):
        if self.debug:
            func_name = inspect.stack()[0][3]
            self.trace(func_name, t)

    def b_selector__variable_name(self, t):
        if self.debug:
            func_name = inspect.stack()[0][3]
            self.trace(func_name, t)
            
        self.curr_var_name = str(t[0])

    def b_selector__variable_select(self, t):
        if self.debug:
            func_name = inspect.stack()[0][3]
            self.trace(func_name, t)
            
        key = self.curr_selector + "::" + self.curr_var_name
        
        self.selector_var[key] = str(t[0])

    def b_selector__close_selector_block(self, t):
        if self.debug:
            func_name = inspect.stack()[0][3]
            self.trace(func_name, t)

        # issue 55 : for all variables which have typ values, but they are not in the Selector
        for key in self.var_typ_value.keys():
            s = key.split("::")
            key = self.curr_selector + "::" + s[1]
            self.selector_var[key] = "Typ"
        
            
        self.curr_selector = DomainUtils.global_domain
