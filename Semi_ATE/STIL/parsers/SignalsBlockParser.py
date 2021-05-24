# -*- coding: utf-8 -*-
import inspect

class SignalsBlockParser:
    def __init__(self, debug=True):
        self.debug = debug
#       dict key   is the signal name
#       dict value is the signal type
        self.sig2type = {}
        self.last_signal = ""
       
    def trace(self, func_name, t):
        print(
            f'{__name__}:{func_name} token value "{t}" at line {t.line} column {t.column}'
        )

    def b_signals__OPEN_SIGNAL_BLOCK(self, t):
        if self.debug:
            func_name = inspect.stack()[0][3]
            self.trace(func_name, t)

    def b_signals__SIGNAL_NAME(self, t):
        if self.debug:
            func_name = inspect.stack()[0][3]
            self.trace(func_name, t)
        if t in self.sig2type:
            err_msg = f'Signal {t} already defined! Signal names in Signals block must be unique.'
            raise Exception(err_msg)
        else:                
            self.sig2type[t] = ''
            self.last_signal = str(t)

    def b_signals__SIGNAL_TYPE(self, t):
        if self.debug:
            func_name = inspect.stack()[0][3]
            self.trace(func_name, t)
        
        self.sig2type[self.last_signal] = t
        self.last_signal = ""

    def b_signals__CLOSE_SIGNAL_BLOCK(self, t):
        if self.debug:
            func_name = inspect.stack()[0][3]
            self.trace(func_name, t)

            print("Found signals in the Signal block:")            
            for signal_name in self.sig2type:
                print(f" Signal {signal_name} has type {self.signals[signal_name]}")            
