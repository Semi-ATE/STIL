# -*- coding: utf-8 -*-
import inspect

class SpecBlockParser:
    def __init__(self, debug=False):
        self.debug = debug

        self.curr_var_name = None
        self.curr_var_type = None
        self.curr_category = 'NONE'

        # key is category::variable      
        # If category is not used, the value will be "NONE"
        # value is the variable value        
        self.var_min_value = {}
        self.var_typ_value = {}
        self.var_max_value = {}

        self.variables = []

    def trace(self, func_name, t):
        head = f"{__name__}:{func_name}"

        if isinstance(t, list):
            print(f"{head} rule value {t}")
        else:
            print(f'{head} token value "{t}" at line {t.line} column {t.column}')

    def b_spec__SPEC_DOMAIN_NAME(self, t):
        if self.debug:
            func_name = inspect.stack()[0][3]
            self.trace(func_name, t)

    def b_spec__open_spec_block(self, t):
        if self.debug:
            func_name = inspect.stack()[0][3]
            self.trace(func_name, t)

    def b_spec__cat_name(self, t):
        if self.debug:
            func_name = inspect.stack()[0][3]
            self.trace(func_name, t)

        self.curr_category = str(t[0])

    def b_spec__var_name(self, t):
        if self.debug:
            func_name = inspect.stack()[0][3]
            self.trace(func_name, t)

        self.curr_var_name = str(t[0])
        
        if self.curr_var_name not in self.variables:
            self.variables.append(self.curr_var_name)

    def b_spec__var_typ_value(self, t):
        if self.debug:
            func_name = inspect.stack()[0][3]
            self.trace(func_name, t)
            
        key = self.curr_category + "::" + self.curr_var_name
        value = str(t[0]).replace('\'','')
        self.var_typ_value[key] = value

    def b_spec__var_type(self, t):
        if self.debug:
            func_name = inspect.stack()[0][3]
            self.trace(func_name, t)
        
        self.curr_var_type = str(t[0])

    def b_spec__var_value(self, t):
        if self.debug:
            func_name = inspect.stack()[0][3]
            self.trace(func_name, t)
            
        key = self.curr_category + "::" + self.curr_var_name
        value = str(t[0]).replace('\'','')
            
        if self.curr_var_type == "Min":
            self.var_min_value[key] = value
        elif self.curr_var_type == "Typ":
            self.var_typ_value[key] = value
        elif self.curr_var_type == "Max":
            self.var_max_value[key] = value
                    
            
    def b_spec__close_category_block(self, t):
        if self.debug:
            func_name = inspect.stack()[0][3]
            self.trace(func_name, t)

        self.curr_category = 'None'

    def b_spec__close_spec_block(self, t):
        if self.debug:
            func_name = inspect.stack()[0][3]
            self.trace(func_name, t)
