# -*- coding: utf-8 -*-
import inspect


class SignalsBlockParser:
    def __init__(self, debug=False):
        self.debug = debug
        # dict key   is the signal name
        # dict value is the signal type
        self.sig2type = {}
        # Current processing signal
        self.curr_signal = ""

        self.is_signal_block_defined = False

        # dict key   is the signal name
        # dict value is the default drive state of the signal if not used
        self.sig2def_state = {}

        # List of scan in signals defined in the signals block
        self.scanin_sigs = []

        # List of scan out signals defined in the signals block
        self.scanout_sigs = []

    def trace(self, func_name, t):
        head = f"{__name__}:{func_name}"

        if isinstance(t, list):
            print(f"{head} rule value {t}")
        else:
            print(f'{head} token value "{t}" at line {t.line} column {t.column}')

    def b_signals__open_signal_block(self, t):
        if self.debug:
            func_name = inspect.stack()[0][3]
            self.trace(func_name, t)

        if self.is_signal_block_defined:
            err_msg = "Duplication of Signals block found. Only one is allowed !"
            raise Exception(err_msg)

        self.is_signal_block_defined = True

    def b_signals__SIGNAL_NAME(self, t):
        if self.debug:
            func_name = inspect.stack()[0][3]
            self.trace(func_name, t)
        if t.value in self.sig2type:
            err_msg = f"Signal {t} already defined! Signal names in Signals block must be unique."
            raise Exception(err_msg)
        else:
            self.sig2type[t] = ""
            self.curr_signal = t.value

    def b_signals__SIGNAL_TYPE(self, t):
        if self.debug:
            func_name = inspect.stack()[0][3]
            self.trace(func_name, t)

        self.sig2type[self.curr_signal] = t.value
        
        
    def b_signals__KEYWORD_SCANIN(self, t):
        if self.debug:
            func_name = inspect.stack()[0][3]
            self.trace(func_name, t)
        
        if self.curr_signal not in self.scanin_sigs:
            self.scanin_sigs.append(self.curr_signal)
        
    def b_signals__KEYWORD_SCANOUT(self, t):
        if self.debug:
            func_name = inspect.stack()[0][3]
            self.trace(func_name, t)

        if self.curr_signal not in self.scanout_sigs:
            self.scanout_sigs.append(self.curr_signal)

    def b_signals__SIGNAL_END_STMT(self, t):
        self.curr_signal = ""
        
    def b_signals__close_signal_attr_block(self, t):
        self.curr_signal = ""        

    def b_signals__SIG_DEF_STATE_UP(self, t):
        if self.debug:
            func_name = inspect.stack()[0][3]
            self.trace(func_name, t)

        self.sig2def_state[self.curr_signal] = "U"

    def b_signals__SIG_DEF_STATE_DOWN(self, t):
        if self.debug:
            func_name = inspect.stack()[0][3]
            self.trace(func_name, t)

        self.sig2def_state[self.curr_signal] = "D"

    def b_signals__SIG_DEF_STATE_OFF(self, t):
        if self.debug:
            func_name = inspect.stack()[0][3]
            self.trace(func_name, t)

        self.sig2def_state[self.curr_signal] = "Z"

    def b_signals__close_signal_block(self, t):
        if self.debug:
            func_name = inspect.stack()[0][3]
            self.trace(func_name, t)

            print("Found signals in the Signal block:")
            for signal_name in self.sig2type:
                print(f" Signal {signal_name} has type {self.sig2type[signal_name]}")
