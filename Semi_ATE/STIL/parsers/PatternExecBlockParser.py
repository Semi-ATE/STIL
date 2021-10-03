# -*- coding: utf-8 -*-
import inspect

from .DomainUtils import DomainUtils


class PatternExecBlockParser:
    def __init__(self, debug=False):
        self.debug = debug

        # dict key   is the pattern exec block name
        # dict value is a list with pattern burst blocks
        self.patt_exec_block2patt_burst = {}

        self.curr_patt_exec = DomainUtils.global_domain

        self.curr_timing_domain = DomainUtils.global_domain

        # List with names of all pattern block which should be executed
        self.used_patterns = []

        # dict key   is the pattern exec block name
        # dict value is the timing domain
        self.patt_exec_block2time_domain = {}

        self.is_patternexec_block_defined = False

    def trace(self, func_name, t):
        head = f"{__name__}:{func_name}"

        if isinstance(t, list):
            print(f"{head} rule value {t}")
        else:
            print(f'{head} token value "{t}" at line {t.line} column {t.column}')

    def b_pattern_exec__PATTERN_EXEC_BLOCK_NAME(self, t):

        if self.debug:
            func_name = inspect.stack()[0][3]
            self.trace(func_name, t)

        if t in self.patt_exec_block2patt_burst:
            err_msg = f"Pattern exec block {t} already defined! Pattern exec block name must be unique."
            raise Exception(err_msg)
        else:
            self.patt_exec_block2patt_burst[t.value] = []
            self.curr_patt_exec = t.value

    def b_pattern_exec__OPEN_PATTERN_EXEC_BLOCK(self, t):
        if self.debug:
            func_name = inspect.stack()[0][3]
            self.trace(func_name, t)

        if self.is_signal_block_defined == False:
            err_msg = "Expected Signal block before any PatternExec block"
            raise Exception(err_msg)
        if self.is_signalgroups_block_defined == False:
            err_msg = "Expected SignalGroups block before any PatternExec block"
            raise Exception(err_msg)
        if self.is_timing_block_defined == False:
            err_msg = "Expected Timing block before any PatternExec block"
            raise Exception(err_msg)
        if self.is_patternburst_block_defined == False:
            err_msg = "Expected PatternBurst block before any PatternExec block"
            raise Exception(err_msg)
        self.is_patternexec_block_defined = True

        global_domain = DomainUtils.global_domain

        if global_domain in self.patt_exec_block2patt_burst:
            err_msg = "Only one global PatternExec block can exists!"
            raise Exception(err_msg)

        if self.curr_patt_exec == global_domain:
            self.patt_exec_block2patt_burst[self.curr_patt_exec] = []

    def b_pattern_exec__PATTERN_BURST_NAME(self, t):
        if self.debug:
            func_name = inspect.stack()[0][3]
            self.trace(func_name, t)

        patt_burst_name = t.value

        if patt_burst_name not in self.patt_burst_block2pattern_blocks:
            err_msg = f"Pattern burst block named {patt_burst_name} is not defined!"
            raise Exception(err_msg)

        burst_names = self.patt_exec_block2patt_burst[self.curr_patt_exec]
        burst_names.append(patt_burst_name)

        patterns = self.patt_burst_block2pattern_blocks.get(patt_burst_name)
        for pattern in patterns:

            if pattern not in self.used_patterns:
                self.used_patterns.append(pattern)

            if pattern not in self.patt2timing_domain:
                self.patt2timing_domain[pattern] = [self.curr_timing_domain]
            else:
                domains = self.patt2timing_domain[pattern]
                if self.curr_timing_domain not in domains:
                    if domains is None:
                        self.patt2timing_domain[pattern] = [self.curr_timing_domain]
                    else:
                        domains.append(self.curr_timing_domain)

        macro_domain = self.patt_burst2macro_domain[patt_burst_name]
        if macro_domain in self.macro_domain2timing_domain:
            l = self.macro_domain2timing_domain[macro_domain]
            if self.curr_timing_domain not in l:
                l.append(self.curr_timing_domain)
        else:
            self.macro_domain2timing_domain[macro_domain] = [self.curr_timing_domain]

        proc_domain = self.patt_burst2proc_domain[patt_burst_name]
        if proc_domain in self.proc_domain2timing_domain:
            l = self.proc_domain2timing_domain[proc_domain]
            if self.curr_timing_domain not in l:
                l.append(self.curr_timing_domain)
        else:
            self.proc_domain2timing_domain[proc_domain] = [self.curr_timing_domain]

    def b_pattern_exec__TIMING_DOMAIN(self, t):
        if self.debug:
            func_name = inspect.stack()[0][3]
            self.trace(func_name, t)
        self.curr_timing_domain = t.value

        if self.curr_timing_domain not in self.time_domain2wft:
            err_msg = f"Timing domain {self.curr_timing_domain} is not defined!"
            raise Exception(err_msg)

    def b_pattern_exec__CLOSE_PATTERN_EXEC_BLOCK(self, t):
        if self.debug:
            func_name = inspect.stack()[0][3]
            self.trace(func_name, t)

        self.patt_exec_block2time_domain[self.curr_patt_exec] = self.curr_timing_domain

        self.curr_patt_exec = DomainUtils.global_domain
        self.curr_timing_domain = DomainUtils.global_domain
