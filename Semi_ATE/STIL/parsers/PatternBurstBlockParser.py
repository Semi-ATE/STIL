# -*- coding: utf-8 -*-
import inspect


from .DomainUtils import DomainUtils


class PatternBurstBlockParser:
    def __init__(self, debug=False):
        self.debug = debug

        # List with all pattern burst block names
        self.patt_burst_names = []

        # dict key   is the pattern burst block name
        # dict value is a list with pattern blocks
        self.patt_burst_block2pattern_blocks = {}

        # dict key   is the pattern name
        # dict value is lark token object which holds the pattern name
        self.patt2obj = {}

        # dict key   is the macrodefs domain name
        # dict value is lark token object which holds the macrodefs domain name
        self.macro_domain2obj = {}

        # dict key   is the procedures domain name
        # dict value is lark token object which holds the procedure domain name
        self.proc_domain2obj = {}

        # dict key   is the pattern burst name
        # dict value is macrodefs domain name
        self.patt_burst2macro_domain = {}

        # dict key   is the pattern burst name
        # dict value is procedures domain name
        self.patt_burst2proc_domain = {}

        # dict key   is the pattern burst name
        # dict value is signal groups domain name
        self.patt_burst2sig_groups_domain = {}

        self.curr_patt_burst = ""

        # dict key   is the pattern name
        # dict value is a list with all signal groups domain defined for this pattern name
        self.patt2sig_group_domain = {}

        self.curr_sig_group_domain = DomainUtils.global_domain

        # dict key   is the pattern name
        # dict value is a list with all timing domains defined for this pattern name in the pattern exec block
        self.patt2timing_domain = {}

        # dict key   is the macro domain
        # dict value is a list with all timing domains defined for this macro domain in the pattern exec block
        self.macro_domain2timing_domain = {}

        # dict key   is the procedure domain
        # dict value is a list with all timing domains defined for this procedure domain in the pattern exec block
        self.proc_domain2timing_domain = {}

        self.is_patternburst_block_defined = False

    def trace(self, func_name, t):
        head = f"{__name__}:{func_name}"

        if isinstance(t, list):
            print(f"{head} rule value {t}")
        else:
            print(f'{head} token value "{t}" at line {t.line} column {t.column}')

    def b_pattern_burst__PATTERN_BURST_BLOCK_NAME(self, t):
        if self.debug:
            func_name = inspect.stack()[0][3]
            self.trace(func_name, t)

        if t.value in self.patt_burst_block2pattern_blocks:
            err_msg = f"Pattern burst block {t} already defined! Pattern burst block names must be unique."
            raise Exception(err_msg)
        else:
            self.patt_burst_block2pattern_blocks[t.value] = []
            self.curr_patt_burst = t.value

        global_domain = DomainUtils.global_domain
        self.last_proc_domain = global_domain
        self.patt_burst2macro_domain[self.curr_patt_burst] = global_domain
        self.patt_burst2proc_domain[self.curr_patt_burst] = global_domain
        self.patt_burst2sig_groups_domain[self.curr_patt_burst] = global_domain

    def b_pattern_burst__open_pattern_burst_block(self, t):
        if self.debug:
            func_name = inspect.stack()[0][3]
            self.trace(func_name, t)

        if self.is_signal_block_defined == False:
            err_msg = "Expected Signal block before any PatternBurst block"
            raise Exception(err_msg)
        if self.is_signalgroups_block_defined == False:
            err_msg = "Expected SignalGroups block before any PatternBurst block"
            raise Exception(err_msg)
        if self.is_timing_block_defined == False:
            err_msg = "Expected Timing block before any PatternBurst block"
            raise Exception(err_msg)
        self.is_patternburst_block_defined = True

        if self.curr_patt_burst in self.patt_burst_names:
            err_msg = f"Pattern burst name '{self.curr_patt_burst}' is already defined"
            raise Exception(err_msg)
        else:
            self.patt_burst_names.append(self.curr_patt_burst)

    def b_pattern_burst__PATT_OR_BURST_NAME(self, t):
        if self.debug:
            func_name = inspect.stack()[0][3]
            self.trace(func_name, t)
        patt_burst_block = self.patt_burst_block2pattern_blocks[self.curr_patt_burst]
        # Collect pattern token to check later if it is defined at the end of the file
        self.patt2obj[t.value] = t
        
        if t.value not in self.patt_burst_names:
            patt = t.value
            patt_burst_block.append(patt)
            if patt in self.patt2sig_group_domain:
                sig_group_list = self.patt2sig_group_domain[t.value]
                if self.curr_sig_group_domain not in sig_group_list:
                    sig_group_list.append(self.curr_sig_group_domain)
            else:
                self.patt2sig_group_domain[patt] = [self.curr_sig_group_domain]
        else:
            err_msg = f"No support so far for pattern burst reference {t.value} in pattern burst block"
            raise Exception(err_msg)
        

    def b_pattern_burst__SIGNAL_GROUPS_DOMAIN(self, t):
        if self.debug:
            func_name = inspect.stack()[0][3]
            self.trace(func_name, t)
        self.patt_burst2sig_groups_domain[self.curr_patt_burst] = t.value
        if t.value not in self.signal_groups_domains:
            err_msg = f"Signal Groups domain name {t.value} used in pattern burst {self.curr_patt_burst} is not defined!"
            raise Exception(err_msg)
        self.curr_sig_group_domain = t.value

    #            raise VisitError(err_msg, t, Exception(err_msg))

    def b_pattern_burst__MACROS_DOMAIN(self, t):
        if self.debug:
            func_name = inspect.stack()[0][3]
            self.trace(func_name, t)
        self.patt_burst2macro_domain[self.curr_patt_burst] = t.value
        self.macro_domain2obj[t.value] = t

    def b_pattern_burst__PROCEDURES_DOMAIN(self, t):
        if self.debug:
            func_name = inspect.stack()[0][3]
            self.trace(func_name, t)
        self.patt_burst2proc_domain[self.curr_patt_burst] = t.value
        self.proc_domain2obj[t.value] = t

    def b_pattern_burst__close_pattern_burst_block(self, t):
        if self.debug:
            func_name = inspect.stack()[0][3]
            self.trace(func_name, t)

            print("Found pattern blocks in the PatternBurst block:")
            for key in self.patt_burst_block2pattern_blocks.keys():
                print(f" PatternBurst block {key} ")
                for value in self.patt_burst_block2pattern_blocks[key]:
                    print(f"  => Pattern/Burst block : {value} ")
        self.curr_sig_group_domain = DomainUtils.global_domain
        self.curr_patt_burst = ""
