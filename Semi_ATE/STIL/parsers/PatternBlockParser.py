# -*- coding: utf-8 -*-
import inspect

from lark.exceptions import VisitError
from .WFCUtils import WFCUtils
from .DomainUtils import DomainUtils
from .STILSemanticException import STILSemanticException

class PatternBlockParser:
    def __init__(self, debug=False):
        self.debug = debug

        self.is_first_pattern = False
        self.is_first_vector = True

        # List with all pattern names
        self.patterns = []
        # Name of the current pattern block
        self.curr_pattern = ""
        # dict key   is the pattern block name
        # dict value is a list with procedure names (without domain name) which are called in this pattern block
        self.patt2call = {}
        # dict key   is the pattern block name
        # dict value is a list with macro names (without domain name) which are called in this pattern block
        self.patt2macro = {}

        # Current signal/signal group
        self.curr_sig_ref = ""
        # Current WFC data
        self.curr_vec_data = ""
        # Current WFT
        self.curr_wft = ""

        self.curr_macro_name_call = ""
        self.curr_proc_name_call = ""

        # dict key   is the pattern name together with signals group domain -> SignalsGroupDomain::pattern_name
        # dict value is a list with signal names found in the first vector address
        self.patt2sig_order = {}

        # List of signals/signal groups for the current vector address
        self.curr_sig_order = []
        # List of WFC for the current vector address
        self.curr_wfc_order = []

        # dict key   is the pattern name
        # dict value is a list with all found labels in this pattern
        self.patt_labels = {}
        # dict key   is the pattern name
        # dict value is a list with all found goto labels in this pattern
        self.patt_goto_labels = {}
        # dict key   is the label name of the goto statement
        # dict value is the goto label object
        self.goto_label_obj = {}
        
        self.keywords_in_patt_block = ["V", "Vector", 
                                       "C", "Condition", 
                                       "F", "Fixed",
                                       "Loop", "MatchLoop", "Infinite",
                                       "Macro", "Call", "BreakPoint", "Goto",
                                       "Stop", "IDDQTestPoint", "IddqTestPoint",
                                       "ScanChain","ActiveScanChains"
                                       ]

    def trace(self, func_name, t):
        head = f"{__name__}:{func_name}"

        if isinstance(t, list):
            print(f"{head} rule value {t}")
        else:
            print(f'{head} token value "{t}" at line {t.line} column {t.column}')


    def b_pattern__pattern_statements__USER_KEYWORD_NAME(self, t):
        if self.debug:
            func_name = inspect.stack()[0][3]
            self.trace(func_name, t)
        
        if t.value not in self.user_defined_keywords:
            err_msg = f"User keyword {t.value} is not defined!"
            raise Exception(err_msg)
        
    def b_pattern__PATTERN_NAME(self, t):
        if self.debug:
            func_name = inspect.stack()[0][3]
            self.trace(func_name, t)

        if t in self.patterns:
            err_msg = f"Pattern block {t} already defined! Pattern block names must be unique."
            raise Exception(err_msg)
        else:
            self.curr_pattern = t.value
            self.patterns.append(self.curr_pattern)
            self.patt2call[self.curr_pattern] = []
            self.patt2macro[self.curr_pattern] = []
            self.patt_labels[self.curr_pattern] = []
            self.patt_goto_labels[self.curr_pattern] = []
            self.goto_label_obj = {}

    def b_pattern__open_pattern_block(self, t):
        if self.debug:
            func_name = inspect.stack()[0][3]
            self.trace(func_name, t)

        if self.is_signal_block_defined == False:
            err_msg = "Expected Signal block before any Pattern block"
            raise Exception(err_msg)
        if self.is_signalgroups_block_defined == False:
            err_msg = "Expected SignalGroups block before any Pattern block"
            raise Exception(err_msg)
        if self.is_timing_block_defined == False:
            err_msg = "Expected Timing block before any Pattern block"
            raise Exception(err_msg)
        if self.is_patternburst_block_defined == False:
            err_msg = "Expected PatternBurst block before any Pattern block"
            raise Exception(err_msg)
        if self.is_patternexec_block_defined == False:
            err_msg = "Expected PatternExec block before any Pattern block"
            raise Exception(err_msg)

        if self.is_first_pattern == False:
            self.is_first_pattern = True

            """
            # Check if all macro/procedures domains used in PatternBurst are defined
            # For every pattern exec block
            for pattern_exec_block in self.patt_exec_block2patt_burst.keys():
                patt_bursts = self.patt_exec_block2patt_burst[pattern_exec_block]
                # For every pattern burst block in the pattern exec block
                for patt_burst in patt_bursts:
                    proc_domain = self.patt_burst2proc_domain[patt_burst]
                    if proc_domain not in self.proc_domain2proc_names:
                        err_msg = f"Procedure domain '{proc_domain}' is not defined in pattern burst {patt_burst}"
                        raise Exception(err_msg)
                    macro_domain = self.patt_burst2macro_domain[patt_burst]
                    if macro_domain not in self.macro_domain2macro_names:
                        print(
                            f"macro_domain {macro_domain} {self.macro_domain2obj} {self.macro_domain2obj[macro_domain].line}"
                        )
                        err_msg = f"MacroDefs domain '{macro_domain}' used in the pattern burst block {patt_burst} is not defined !"
                        raise VisitError(
                            err_msg,
                            self.macro_domain2obj[macro_domain],
                            Exception(err_msg),
                        )
            """
        self.va = 0

    def b_pattern__pattern_statements__WAVEFORM_TABLE_NAME(self, t):
        if self.debug:
            func_name = inspect.stack()[0][3]
            self.trace(func_name, t)

        wft_name = t.value
        self.curr_wft = wft_name

        for pattern_exec_block in self.patt_exec_block2patt_burst.keys():
            patt_bursts = self.patt_exec_block2patt_burst[pattern_exec_block]
            # For every pattern burst block in the pattern exec block
            for patt_burst in patt_bursts:

                pattern_list = self.patt_burst_block2pattern_blocks[patt_burst]

                # For every pattern block in the pattern burst block
                for pattern in pattern_list:

                    if pattern != self.curr_pattern:
                        continue

                    time_domain = self.patt_exec_block2time_domain[pattern_exec_block]
                    wft_list = self.time_domain2wft[time_domain]
                    if wft_name not in wft_list:
                        td = DomainUtils.get_domain(time_domain, True)
                        err_msg = f"Wafeform Table named '{wft_name}' from '{td}' timing domain is not defined !"
                        raise Exception(err_msg)
    
    def b_pattern__pattern_statements__CALL_PROC_NAME(self, t):
        if self.debug:
            func_name = inspect.stack()[0][3]
            self.trace(func_name, t)        

    def b_pattern__pattern_statements__CALL_MACRO_NAME(self, t):
        if self.debug:
            func_name = inspect.stack()[0][3]
            self.trace(func_name, t)        

    def b_pattern__pattern_statements__KEYWORD_V(self, t):
        if self.debug:
            func_name = inspect.stack()[0][3]
            self.trace(func_name, t)

        self.is_vector_stmt = True

    def b_pattern__pattern_statements__KEYWORD_VECTOR(self, t):
        if self.debug:
            func_name = inspect.stack()[0][3]
            self.trace(func_name, t)

        self.is_vector_stmt = True

    def b_pattern__pattern_statements__LABEL(self, t):
        if self.debug:
            func_name = inspect.stack()[0][3]
            self.trace(func_name, t)

        if t.value[-1] == ':':
            label_str = t.value[0:-1]
        else:
            label_str = t.value
        label_strip = label_str.strip()
        if label_strip.startswith('"') == False and label_strip.endswith('"') == False:
            label_split = label_strip.split(" ")
            label = label_split[0].strip()
            if label in self.keywords_in_patt_block:
                err_msg = f"Label '{label}' is a reserved keyword !"
                raise Exception(err_msg)
                
        else:
            label = label_strip
            
        labels = self.patt_labels[self.curr_pattern]
        if label in labels:
            err_msg = f"Label '{label}' is already defined !"
            raise Exception(err_msg)
        else:
            labels.append(label)

        return label

    def b_pattern__pattern_statements__GOTO_LABEL(self, t):
        if self.debug:
            func_name = inspect.stack()[0][3]
            self.trace(func_name, t)

        gt_label = t.value
        labels = self.patt_goto_labels[self.curr_pattern]
        if gt_label not in labels:
            labels.append(gt_label)
        
        self.goto_label_obj[gt_label] = t

    def b_pattern__pattern_statements__SIGREF_EXPR(self, t):
        if self.debug:
            func_name = inspect.stack()[0][3]
            self.trace(func_name, t)
        self.curr_sig_ref = t.value

        self.curr_sig_order.append(self.curr_sig_ref)

    def b_pattern__pattern_statements__VEC_DATA_STRING(self, t):
        if self.debug:
            func_name = inspect.stack()[0][3]
            self.trace(func_name, t)

        vec_data = WFCUtils.expand_wfcs(t.value)

        self.curr_wfc_order.append(vec_data)

        sigref = self.curr_sig_ref

        if self.curr_sig_ref in self.sig2type:
            # Check if WFC is defined for the signal
            if len(vec_data) > 1:
                err_msg = f"Signal '{self.curr_sig_ref}' has more than one WFC !"
                raise Exception(err_msg)
            sig = self.curr_sig_ref
            if self.curr_pattern in self.patt2timing_domain:
                tds = self.patt2timing_domain[self.curr_pattern]
                for d in tds:
                    indx = 0
                    dn = DomainUtils.get_domain(d, True)
                    fstn = DomainUtils.get_full_name(d, sig)
                    if fstn in self.sig2wfc:
                        wfc_list = self.sig2wfc[fstn]
                        wfc = vec_data[indx : indx + 1]
                        if wfc not in wfc_list:
                            err_msg = f"Not defined WFC '{wfc}' for signal {sig} for the '{dn}' domain!"
                            raise Exception(err_msg)
                        indx += 1
                    else:
                        pass
                        # ToDo!!!
                        # err_msg = f"Signal '{sig}' does not have WFCs defined in timing domain '{dn}'!"
                        # raise Exception(err_msg)
        else:
            # check if sigref is already defined signal group

            if self.curr_pattern in self.used_patterns:

                if self.curr_pattern in self.patt2sig_group_domain:

                    sig_group_domains = self.patt2sig_group_domain[self.curr_pattern]

                    is_signal_group_found = False

                    for sig_group_domain in sig_group_domains:

                        sig_group_name = DomainUtils.get_full_name(
                            sig_group_domain, sigref
                        )
                        sig_groups = self.signal_groups2signals.keys()

                        for sig_group in sig_groups:
                            sgd = DomainUtils.get_domain(sig_group)
                            if sgd != sig_group_domain:
                                continue
                            sig_group_name = DomainUtils.get_name(sig_group)
                            if sig_group_name == sigref:
                                is_signal_group_found = True
                                signals = self.signal_groups2signals.get(sig_group)
                                # check if signal length corresponds to the WFC length
                                if len(signals) != len(vec_data):
                                    domain = DomainUtils.get_domain(sig_group, True)
                                    err_msg = f"Number of WFC ({len(vec_data)}) does not match with the number of signals ({len(signals)}) for signal groups '{sig_group_name}' in {domain} domain!"
                                    raise Exception(err_msg)
                                else:
                                    # Check if WFC are defined for the signal
                                    if self.curr_pattern in self.patt2timing_domain:
                                        tds = self.patt2timing_domain[self.curr_pattern]
                                        for d in tds:
                                            indx = 0
                                            for sig in signals:
                                                fstn = DomainUtils.get_full_name(d, sig)
                                                if fstn not in self.sig2wfc:
                                                    dn = DomainUtils.get_domain(d, True)
                                                    err_msg = f"Signal {sig} is not defined in the {dn} Timing block!"
                                                    raise Exception(err_msg)
                                                wfc_list = self.sig2wfc[fstn]
                                                wfc = vec_data[indx : indx + 1]
                                                if wfc not in wfc_list:
                                                    dn = DomainUtils.get_domain(d, True)
                                                    err_msg = f"Not defined WFC '{wfc}' for signal {sig} in the signal groups '{sig_group_name}' for the '{dn}' domain!"
                                                    raise Exception(err_msg)
                                                indx += 1
                    if is_signal_group_found == False:
                        err_msg = f"Signal/Signal group {sigref} is not defined!"
                        raise Exception(err_msg)
                            

                else:
                    # pattern is not used
                    pass

    def b_pattern__pattern_statements__close_vector_block(self, t):
        if self.debug:
            func_name = inspect.stack()[0][3]
            self.trace(func_name, t)
        
        #Ignore so far the Fixed and Condition statetments        
        if self.is_vector_stmt:

            # Collect signal order for the first vector address
            if self.is_first_vector:
                self.is_first_vector = False
                # print(f"\n=> {self.curr_pattern}")
                if self.curr_wft == "":
                    err_msg = (
                        "Missing WaveformTable reference before the first vector address!"
                    )
                    raise Exception(err_msg)
            self.curr_wft = ""

        self.curr_sig_order = []
        self.curr_wfc_order = []

        self.curr_sig_ref = ""
        self.curr_vec_data = ""
        self.is_vector_stmt = False

    def b_pattern__pattern_statements__CALL_PROC_NAME(self, t):
        if self.debug:
            func_name = inspect.stack()[0][3]
            self.trace(func_name, t)
        self.patt2call[self.curr_pattern].append(t.value)
        self.curr_proc_name_call = t.value

        # Check if procedure is defined for all procedures domains
        for pattern_exec_block in self.patt_exec_block2patt_burst.keys():
            patt_bursts = self.patt_exec_block2patt_burst[pattern_exec_block]
            # For every pattern burst block in the pattern exec block
            for patt_burst in patt_bursts:
                pattern_list = self.patt_burst_block2pattern_blocks[patt_burst]
                # For every pattern block in the pattern burst block
                for pattern in pattern_list:
                    proc_domain = self.patt_burst2proc_domain[patt_burst]
                    if proc_domain in self.proc_domain2proc_names:
                        proc_names_defines = self.proc_domain2proc_names[proc_domain]
                        if pattern in self.patt2call:
                            proc_calls = self.patt2call[pattern]
                            for proc_name_call in proc_calls:

                                if proc_name_call not in proc_names_defines:

                                    if proc_domain == DomainUtils.global_domain:
                                        err_msg = f"Procedure {proc_name_call} called in the pattern {pattern} is not defined in the global procedure domain !"
                                    else:
                                        err_msg = f"Procedure {proc_name_call} called in the pattern {pattern} is not defined in the procedure domain {proc_domain} !"
                                    raise Exception(err_msg)
                    else:
                        if proc_domain == DomainUtils.global_domain:
                            err_msg = f"Unnamed (global) Procedures block is not defined for Procedure named '{self.curr_proc_name_call}' called in the pattern {pattern} !"
                        else:
                            line = self.proc_domain2obj[proc_domain].line
                            err_msg = f"Procedures block '{proc_domain}' in line {line} is not defined for Procedure named '{self.curr_proc_name_call}' called in the pattern {pattern} !"
                        raise Exception(err_msg)

    def b_pattern__pattern_statements__CALL_MACRO_NAME(self, t):
        if self.debug:
            func_name = inspect.stack()[0][3]
            self.trace(func_name, t)
        self.patt2macro[self.curr_pattern].append(t.value)
        self.curr_macro_name_call = t.value

        # Check if macro is defined for all macro domains
        for pattern_exec_block in self.patt_exec_block2patt_burst.keys():
            patt_bursts = self.patt_exec_block2patt_burst[pattern_exec_block]
            # For every pattern burst block in the pattern exec block
            for patt_burst in patt_bursts:
                pattern_list = self.patt_burst_block2pattern_blocks[patt_burst]
                # For every pattern block in the pattern burst block
                for pattern in pattern_list:
                    macro_domain = self.patt_burst2macro_domain[patt_burst]
                    if macro_domain in self.macro_domain2macro_names:
                        macro_names_defines = self.macro_domain2macro_names[
                            macro_domain
                        ]
                        if pattern in self.patt2macro:
                            macro_calls = self.patt2macro[pattern]

                            for macro_name_call in macro_calls:
                                if macro_name_call not in macro_names_defines:
                                    if macro_domain == DomainUtils.global_domain:
                                        err_msg = f"Macro {macro_name_call} called in the pattern {pattern} is not defined in the unnamed (global) macrodefs domain !"
                                    else:
                                        err_msg = f"Macro {macro_name_call} called in the pattern {pattern} is not defined in the macrodefs domain {macro_domain} !"
                                    raise Exception(err_msg)

                    else:
                        if macro_domain == DomainUtils.global_domain:
                            err_msg = f"Unnamed (global) Macrodefs block is not defined for Macro named '{self.curr_macro_name_call}' called in the pattern {pattern} !"
                        else:
                            line = self.macro_domain2obj[macro_domain].line
                            err_msg = f"Macrodefs block '{macro_domain}' in line {line} is not defined for Macro named '{self.curr_macro_name_call}' called in the pattern {pattern} !"
                        raise Exception(err_msg)

    def b_pattern__pattern_statements__CALL_SIGREF_EXPR(self, t):
        if self.debug:
            func_name = inspect.stack()[0][3]
            self.trace(func_name, t)
        self.curr_sig_ref = t.value
        # print(f"\n===> CALL_SIGREF_EXPR {t.value}\n")

        sigref = self.curr_sig_ref

        if sigref in self.sig2type:
            # signal ref is defined in the Signal block
            pass
        else:
            # check if sigref is already defined signal group
            # get all signal groups domain for the current pattern
            sig_group_domains = self.patt2sig_group_domain[self.curr_pattern]
            for sig_group_domain in sig_group_domains:

                sig_group_name = DomainUtils.get_full_name(sig_group_domain, sigref)
                sig_groups = self.signal_groups2signals.keys()

                if sig_group_name not in sig_groups:
                    if sig_group_domain == DomainUtils.global_domain:
                        sig_group_domain = "unnamed"
                    err_msg = f"In the '{sig_group_domain}' signal group domain, there is no definition for signal reference '{self.curr_sig_ref}' used in the pattern block '{self.curr_pattern}' !"
                    raise Exception(err_msg)

    def b_pattern__pattern_statements__CALL_VEC_DATA_STRING(self, t):
        if self.debug:
            func_name = inspect.stack()[0][3]
            self.trace(func_name, t)
        self.curr_sig_ref = ""

    def b_pattern__pattern_statements__MACRO_SIGREF_EXPR(self, t):
        if self.debug:
            func_name = inspect.stack()[0][3]
            self.trace(func_name, t)
        self.curr_sig_ref = t.value

    def b_pattern__pattern_statements__MACRO_VEC_DATA_STRING(self, t):
        if self.debug:
            func_name = inspect.stack()[0][3]
            self.trace(func_name, t)
        self.curr_sig_ref = ""

    def b_pattern__pattern_statements__LOOP_COUNT(self, t):
        if self.debug:
            func_name = inspect.stack()[0][3]
            self.trace(func_name, t)
        if int(t.value) < 1:
            err_msg = "Loop value must be positive!"
            raise Exception(err_msg)

    def b_pattern__pattern_statements__close_loop_block(self, t):
        if self.debug:
            func_name = inspect.stack()[0][3]
            self.trace(func_name, t)

    def b_pattern__pattern_statements__MATCHLOOP_COUNT(self, t):
        if self.debug:
            func_name = inspect.stack()[0][3]
            self.trace(func_name, t)
        if int(t.value) < 1:
            err_msg = "MatchLoop value must be positive!"
            raise Exception(err_msg)
        
    def b_pattern__pattern_statements__MATCHLOOP_INF(self, t):
        if self.debug:
            func_name = inspect.stack()[0][3]
            self.trace(func_name, t)
        

    def b_pattern__pattern_statements__close_matchloop_block(self, t):
        if self.debug:
            func_name = inspect.stack()[0][3]
            self.trace(func_name, t)

    def b_pattern__close_pattern_block(self, t):
        if self.debug:
            func_name = inspect.stack()[0][3]
            self.trace(func_name, t)
        
        labels = self.patt_labels[self.curr_pattern]
        gt_labels = self.patt_goto_labels[self.curr_pattern]
        for label in gt_labels:
            if label not in labels:
                obj = self.goto_label_obj[label]
                err_msg = f"Label '{label}' used by Goto statament in the Pattern block '{self.curr_pattern}' is not defined!"
                raise STILSemanticException( obj.line, obj.column, err_msg)
                

        self.curr_pattern = ""
        self.is_first_vector = True

    def eof(self):
        if self.debug:
            print("On end of the file")

        # Check if all pattern blocks used in pattern burst are defined
        # For every pattern exec block
        for pattern_exec_block in self.patt_exec_block2patt_burst.keys():
            patt_bursts = self.patt_exec_block2patt_burst[pattern_exec_block]
            # For every pattern burst block in the pattern exec block
            for patt_burst in patt_bursts:
                pattern_list = self.patt_burst_block2pattern_blocks[patt_burst]
                # For every pattern block in the pattern burst block
                for pattern in pattern_list:
                    if pattern not in self.patterns:
                        err_msg = f"Pattern block {pattern} used in pattern burst block {patt_burst} is not defined!"
                        raise VisitError(
                            err_msg, self.patt2obj[pattern], Exception(err_msg)
                        )
                # check domain names for macrodefs, procedures and signal groups
                if patt_burst in self.patt_burst2macro_domain:
                    pass
                if patt_burst in self.patt_burst2proc_domain:
                    pass
                if patt_burst in self.patt_burst2sig_groups_domain:
                    pass
