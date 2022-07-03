# -*- coding: utf-8 -*-
import inspect

from .DomainUtils import DomainUtils
from .TimeUtils import TimeUtils

class PatternExecBlockParser:
    def __init__(self, debug=False):
        self.debug = debug
        
        self.op = {'+', '-', '/', '*', '(', ')'}

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

        # dict key   is the pattern exec block name
        # dict value is a list with all spec categories used in this pattern exec
        self.patt_exec2category = {}

        # dict key   is the pattern exec block name
        # dict value is a list with all selectors used in this pattern exec
        self.patt_exec2selector = {}

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

    def b_pattern_exec__open_pattern_exec_block(self, t):
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
            
    def b_pattern_exec__category_name(self, t):
        if self.debug:
            func_name = inspect.stack()[0][3]
            self.trace(func_name, t)
            
        if self.curr_patt_exec in self.patt_exec2category:
            list_cat = self.patt_exec2category[self.curr_patt_exec]
        else:
            list_cat = []
            self.patt_exec2category[self.curr_patt_exec] = list_cat
        list_cat.append(str(t[0]))
            
    def b_pattern_exec__selector_name(self, t):
        if self.debug:
            func_name = inspect.stack()[0][3]
            self.trace(func_name, t)

        if self.curr_patt_exec in self.patt_exec2selector:
            list_sel = self.patt_exec2selector[self.curr_patt_exec]
        else:
            list_sel = []
            self.patt_exec2selector[self.curr_patt_exec] = list_sel
        list_sel.append(str(t[0]))

    def b_pattern_exec__close_pattern_exec_block(self, t):
        if self.debug:
            func_name = inspect.stack()[0][3]
            self.trace(func_name, t)

        self.process_timings()

        self.patt_exec_block2time_domain[self.curr_patt_exec] = self.curr_timing_domain

        self.curr_patt_exec = DomainUtils.global_domain
        self.curr_timing_domain = DomainUtils.global_domain      
        

    def process_timings(self):
        
        for time_wft in self.wft2period:
            period = self.wft2period[time_wft]
#            key = self.curr_patt_exec + "::" + time_wft
#            print(f"key {key} period {period}")
            self.wft2period[time_wft] = self.parse_time_expr(period)
            
        
        # dict key   is the timing_domain::wft::signal_name
        # dict value is a SigTimingInfo object with timing information 
        for tws in self.sig_wft2timing:
            sti = self.sig_wft2timing[tws]
            wfcs = sti.get_wfcs()
            for wfc in wfcs:
                timing = sti.get_timing_for_wfc(wfc)
                for wfe_time in timing:
                    wfe = wfe_time[0]
                    time = wfe_time[1]
                    ftime = self.parse_time_expr(time)
                    sti.replace_timing_for_wfc(wfc, wfe, time, ftime)
        
            
    def get_var_value(self, selectors, categories, variable):

        for category in categories:        
            for selector in selectors:   
                cat_var = category + "::" + variable
                sel_var = selector + "::" + variable
                #print(f"category {category} cat_var {cat_var}")
                if sel_var in self.selector_var:
                    sel = self.selector_var[sel_var]
                    # key is category::variable      
                    if sel == 'Min':
                        key = category + "::" + variable
                        keyn = "NONE::" + variable
                        if key in self.var_min_value:
                            return self.var_min_value[key]
                        elif keyn in self.var_min_value:
                            return self.var_min_value[keyn]
                        else:
                            err_msg = f"ERROR: Can not find 'Min' value for variable '{variable}' in category '{category}'!"
                            raise Exception(err_msg)
                    elif sel == 'Typ':
                        key = category + "::" + variable
                        keyn = "NONE::" + variable
                        if key in self.var_typ_value:
                            return self.var_typ_value[key]
                        elif keyn in self.var_typ_value:
                            return self.var_typ_value[keyn]
                        else:
                            err_msg = f"ERROR: Can not find 'Typ' value for variable '{variable}' in category '{category}'!"
                            raise Exception(err_msg)
                    elif sel == 'Max':
                        key = category + "::" + variable
                        keyn = "NONE::" + variable
                        if key in self.var_max_value:
                            return self.var_max_value[key]
                        elif keyn in self.var_max_value:
                            return self.var_min_value[keyn]
                        else:
                            err_msg = f"ERROR: Can not find 'Max' value for variable '{variable}' in category '{category}'!"
                            raise Exception(err_msg)
                    else:
                        err_msg = f"ERROR: Unknown selector {sel}!"
                        raise Exception(err_msg)
                elif cat_var in self.var_typ_value:
                    return self.var_typ_value[cat_var]

    
        err_msg = f"ERROR: Variable {variable} is not defined in the selector {selector}!"
        raise Exception(err_msg)
            
            
    def parse_time_expr(self, time_expr):
        
        # Check first if the value is simple time:
        is_simple_time = True
        for i in range(0, len(time_expr)):
            char = time_expr[i]
            if char in self.op:
                is_simple_time = False
                break
        
        if is_simple_time:
            fsec = TimeUtils.get_time_fsec(time_expr)
            try:
                value = int(fsec)
                return str(value) + "fs"
            except Exception:
                # The value is spec variable, will be processed in the next lines
                pass
            
        # The time is expressoin, let's calculate it:
        if self.curr_patt_exec in self.patt_exec2category:
            cat = self.patt_exec2category[self.curr_patt_exec]
        elif len(self.var_typ_value) != 0 :
            for var in self.var_typ_value:
                cat2var = var.split("::")
                if cat2var[1] == time_expr:
                    cat.append(cat2var[0])
        else:
            domain_name = DomainUtils.get_domain(self.curr_patt_exec, True)
            err_msg = f"ERROR: Trying to find value for time expression {time_expr}, but Category is missing in the {domain_name} PatternExec block"
            raise Exception(err_msg)

        if self.curr_patt_exec in self.patt_exec2selector:
            sel = self.patt_exec2selector[self.curr_patt_exec]
        elif len(self.var_typ_value) != 0 :
            sel = ["Typ"]
        else:
            domain_name = DomainUtils.get_domain(self.curr_patt_exec, True)
            err_msg = f"ERROR: Trying to find value for time expression {time_expr}, but Selector is missing in the {domain_name} PatternExec block"
            raise Exception(err_msg)
            
        op_list = []

        buff = ""
        for i in range(0, len(time_expr)):
            char = time_expr[i]
            if char.isalnum():
                buff += char
            elif char == ' ':
                pass
            elif char == '_':
                buff += char
            elif char == '.':
                buff += char
            elif char in self.op:
                if buff in self.variables:
                    val = self.get_var_value(sel, cat, buff)
                    buff = val
                if len(buff) > 0:
                    op_list.append(buff)
                if len(char) > 0:
                    op_list.append(char)
                buff = ''
                
        if buff in self.variables:
            val = self.get_var_value(sel, cat, buff)
            if len(val) > 0:
                op_list.append(val)
        else:
            if len(buff) > 0:
                op_list.append(buff)
            
        # Return expression according order of operations
        return TimeUtils.bodmas(op_list, time_expr)

