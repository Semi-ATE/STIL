# -*- coding: utf-8 -*-
import inspect

from .DomainUtils import DomainUtils
from .WFCUtils import WFCUtils
from .HashInfo import HashInfo
from .STILSemanticException import STILSemanticException


class ProceduresBlockParser:
    def __init__(self, debug=False):
        self.debug = debug

        self.is_condition_stmt = False
        self.is_first_vector = True

        # List with all procedures block names
        self.procedures_domains = []

        # dict key   is the procesures domain name
        # dict value is a list with all procesures defined for this domain
        self.proc_domain2proc_names = {}
        # list with procedures names (with domain prefix) which have shift statement
        self.proc_with_shift = []
        # list with procedures names (with domain prefix) which have # or % for substitution
        self.proc_for_subs = []

        # dict key   is domain::procedure_name
        # dict value is vector addresses
        self.proc2va = {}

        # dict key   is domain::procedure_name
        # dict value is test cyclces : ordinary vectors + loops
        self.proc2tc = {}

        # Current domain name
        self.curr_proc_domain = DomainUtils.global_domain
        # current procedure name is in full domain format -> domain::procedure_name
        self.curr_proc_name = ""
        # Current signal/signal group
        self.curr_sig_ref = ""
        # Current WFC data
        self.curr_vec_data = ""
        # Current WFT
        self.curr_wft = ""
        # Position relative to the shift block
        self.pos_rel_shift = HashInfo.POS_UNKNOWN
        # dict key   is the procedures domain name
        # dict value is a list with all HashInfo objects
        self.hashinfo = {}

        # dict key   is the procedure name in full domain format -> domain::procedure_name
        # dict value is a list with signal names found in the first vector address
        self.proc2sig_order = {}

        # List of signals/signal groups for the current vector address
        self.curr_proc_sig_order = []
        # List of WFC for the current vector address
        self.curr_proc_wfc_order = []
        # List of WFC for the current condition statements
        self.curr_proc_cond_wfc_order = []

        # Contains WFC data for signals found in the first Condition statament,
        # before the first vector statement
        # dict key   is the procedure name in full domain format -> domain::proc_name
        # dict value is a dict with key signal name and value WFC 
        self.proc2first_cond = {}

        # Start VA of the loop block
        self.start_loop_va = 0
        # Loop count value
        self.loop_count = 0

        self.is_found_hash_proc = False

        
        self.is_vector_stmt = False
        # dict key   is the procedure name in full domain format -> domain::procedure_name
        # dict value is a list with all found labels in this procedure
        self.proc_labels = {}
        # dict key   is the procedure name in full domain format -> domain::procedure_name
        # dict value is a list with all found goto labels in this procedure
        self.proc_goto_labels = {}
        # dict key   is the label name of the goto statement
        # dict value is the goto label object
        self.proc_goto_label_obj = {}

        # List with signals wich have % as WFC. Signal name in full domain format -> domain::signal_name
        self.proc_sig_wfc_percent = []

        # List with signals wich have # as WFC. Signal name in full domain format -> domain::signal_name
        self.proc_sig_wfc_hash = []
        
        self.keywords_in_proc_block = ["V", "Vector", 
                                       "C", "Condition", 
                                       "F", "Fixed",
                                       "Loop", "MatchLoop", "Infinite",
                                       "Macro", "Call", "BreakPoint", "Goto",
                                       "Stop", "IDDQTestPoint", "IddqTestPoint",
                                       "ScanChain","ActiveScanChains", "Shift"
                                       ]


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
        self.curr_proc_domain = t.value

    def b_procedures__open_procedures_block(self, t):
        if self.debug:
            func_name = inspect.stack()[0][3]
            self.trace(func_name, t)

        if self.curr_proc_domain in self.procedures_domains:
            domain_name = DomainUtils.get_domain(self.curr_proc_domain, True)
            err_msg = f"Procedures block domain '{domain_name}' is already defined !"
            raise Exception(err_msg)
        else:
            self.procedures_domains.append(self.curr_proc_domain)

    def b_procedures__PROCEDURE_NAME(self, t):
        if self.debug:
            func_name = inspect.stack()[0][3]
            self.trace(func_name, t)
        proc_name = t.value
        proc_names = self.proc_domain2proc_names.get(self.curr_proc_domain)
        if proc_names == None:
            proc_names = [proc_name]
            self.proc_domain2proc_names[self.curr_proc_domain] = proc_names
        elif proc_name in proc_names:
            err_msg = f"Procedure {proc_name}' is already defined !"
            raise Exception(err_msg)
        else:
            proc_names.append(proc_name)
        self.curr_proc_name = DomainUtils.get_full_name(self.curr_proc_domain, proc_name)
        self.proc2va[self.curr_proc_name] = 0
        self.proc2tc[self.curr_proc_name] = 0

        self.proc_labels[self.curr_proc_name] = []
        self.proc_goto_labels[self.curr_proc_name] = []
        self.proc_goto_label_obj = {}

        self.proc_sig_wfc_percent = []
        self.proc_sig_wfc_hash = []

    def b_procedures__open_proc(self, t):
        if self.debug:
            func_name = inspect.stack()[0][3]
            self.trace(func_name, t)
        self.pos_rel_shift = HashInfo.POS_BEFORE_SHIFT
        self.va = 0

    def b_procedures__pattern_statements__USER_KEYWORD_NAME(self, t):
        if self.debug:
            func_name = inspect.stack()[0][3]
            self.trace(func_name, t)
        
        if t.value not in self.user_defined_keywords:
            err_msg = f"User keyword {t.value} is not defined!"
            raise Exception(err_msg)

    def b_procedures__pattern_statements__WAVEFORM_TABLE_NAME(self, t):
        if self.debug:
            func_name = inspect.stack()[0][3]
            self.trace(func_name, t)

        wft_name = t.value
        self.curr_wft = wft_name
        
        for pattern_exec_block in self.patt_exec_block2patt_burst.keys():
            patt_bursts = self.patt_exec_block2patt_burst[pattern_exec_block]
            # For every pattern burst block in the pattern exec block
            for patt_burst in patt_bursts:

                proc_domain = self.patt_burst2proc_domain[patt_burst]
                if proc_domain != self.curr_proc_domain:
                    continue

                time_domain = self.patt_exec_block2time_domain[pattern_exec_block]
                wft_list = self.time_domain2wft[time_domain]
                if wft_name not in wft_list:
                    td = DomainUtils.get_domain(time_domain, True)
                    err_msg = f"Wafeform Table named '{wft_name}' from '{td}' timing domain is not defined !"
                    raise Exception(err_msg)

    def b_procedures__pattern_statements__KEYWORD_CONDITION(self, t):
        if self.debug:
            func_name = inspect.stack()[0][3]
            self.trace(func_name, t)
        self.is_condition_stmt = True
    
    def b_procedures__pattern_statements__KEYWORD_C(self, t):
        if self.debug:
            func_name = inspect.stack()[0][3]
            self.trace(func_name, t)
        self.is_condition_stmt = True
        
    def b_procedures__pattern_statements__KEYWORD_V(self, t):
        if self.debug:
            func_name = inspect.stack()[0][3]
            self.trace(func_name, t)
        self.proc2va[self.curr_proc_name] += 1
        self.proc2tc[self.curr_proc_name] += 1
        self.is_vector_stmt = True

    def b_procedures__pattern_statements__KEYWORD_VECTOR(self, t):
        if self.debug:
            func_name = inspect.stack()[0][3]
            self.trace(func_name, t)
        self.proc2va[self.curr_proc_name] += 1
        self.proc2tc[self.curr_proc_name] += 1
        self.is_vector_stmt = True

    def b_procedures__pattern_statements__LABEL(self, t):
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
            if label in self.keywords_in_proc_block:
                err_msg = f"Label '{label}' is a reserved keyword !"
                raise Exception(err_msg)
        else:
            label = label_strip

        labels = self.proc_labels[self.curr_proc_name]
        if label in labels:
            err_msg = f"Label '{label}' is already defined !"
            raise Exception(err_msg)
        else:
            labels.append(label)
            
        return label

    def b_procedures__pattern_statements__GOTO_LABEL(self, t):
        if self.debug:
            func_name = inspect.stack()[0][3]
            self.trace(func_name, t)

        gt_label = t.value
        labels = self.proc_goto_labels[self.curr_proc_name]
        if gt_label not in labels:
            labels.append(gt_label)
        
        self.proc_goto_label_obj[gt_label] = t

    def b_procedures__pattern_statements__SIGREF_EXPR(self, t):
        if self.debug:
            func_name = inspect.stack()[0][3]
            self.trace(func_name, t)
        self.curr_sig_ref = t.value

        if self.curr_sig_ref in self.sig2type:
            # signal ref is defined in the Signal block
            pass
        else:
            # check if sigref is already defined signal group
            # get all signal groups
            if self.curr_sig_ref not in self.all_signal_groups:
                err_msg = f"Signal '{self.curr_sig_ref}' is not defined !"
                raise Exception(err_msg)

        self.curr_proc_sig_order.append(self.curr_sig_ref)

    def b_procedures__pattern_statements__VEC_DATA_STRING(self, t):
        if self.debug:
            func_name = inspect.stack()[0][3]
            self.trace(func_name, t)

        vec_data = WFCUtils.expand_wfcs(t.value)
        
        if self.is_vector_stmt == False:
            self.curr_proc_cond_wfc_order.append(vec_data)

        # Collect increamental substitution information
        pos = WFCUtils.find_hash(vec_data)
        if len(pos) > 0:
            hi = HashInfo(self.pos_rel_shift, self.curr_sig_ref, pos)
            hid = self.hashinfo.get(self.curr_proc_name)
            if hid == None:
                self.hashinfo[self.curr_proc_name] = [hi]
            else:
                hid.append(hi)

        # Check number of WFC against signal/signalgroups
        if self.curr_sig_ref in self.sig2type:
            if len(vec_data) > 1:
                err_msg = f"Signal '{self.curr_sig_ref}' has more than one WFC !"
                raise Exception(err_msg)
            sig = self.curr_sig_ref
            if self.curr_proc_domain in self.proc_domain2timing_domain:
                tds = self.proc_domain2timing_domain[self.curr_proc_domain]
                for d in tds:
                    indx = 0
                    fstn = DomainUtils.get_full_name(d, sig)
                    if fstn not in self.sig2wfc:
                        continue
                    wfc_list = self.sig2wfc[fstn]
                    wfc = vec_data[indx : indx + 1]
                    if wfc == "%":
                        if sig in self.proc_sig_wfc_hash:
                            err_msg = f"Signal '{sig}' can not have both '%' and '#' as WFC!"
                            raise Exception(err_msg)
                        elif sig not in self.proc_sig_wfc_percent:
                            self.proc_sig_wfc_percent.append(sig)
                        fpn = self.curr_proc_name
                        if fpn not in self.proc_for_subs:
                            self.proc_for_subs.append(fpn)
                    elif wfc == "#":
                        if sig in self.proc_sig_wfc_percent:
                            err_msg = f"Signal '{sig}' can not have both '%' and '#' as WFC!"
                            raise Exception(err_msg)
                        elif sig not in self.proc_sig_wfc_hash:
                            self.proc_sig_wfc_hash.append(sig)
                        fpn = self.curr_proc_name
                        if fpn not in self.proc_for_subs:
                            self.proc_for_subs.append(fpn)
                        self.is_found_hash_proc = True
                    elif wfc not in wfc_list:
                        dn = DomainUtils.get_domain(d, True)
                        err_msg = f"Not defined WFC '{wfc}' for signal {sig} for the '{dn}' domain!"
                        raise Exception(err_msg)
                    indx += 1
        else:
            for pattern_exec_block in self.patt_exec_block2patt_burst.keys():
                patt_bursts = self.patt_exec_block2patt_burst[pattern_exec_block]
                # For every pattern burst block in the pattern exec block
                for patt_burst in patt_bursts:
                    sig_group_domain = self.patt_burst2sig_groups_domain[patt_burst]

                    proc_domain = self.patt_burst2proc_domain[patt_burst]

                    if proc_domain != self.curr_proc_domain:
                        continue

                    fsg = DomainUtils.get_full_name(sig_group_domain, self.curr_sig_ref)
                    domain = DomainUtils.get_domain(fsg, True)

                    if fsg in self.signal_groups2signals:
                        signals = self.signal_groups2signals[fsg]
                        if len(signals) != len(vec_data):
                            #pass
                            err_msg = f"Number of WFC ({len(vec_data)}) does not match with the number of signals ({len(signals)}) for signal groups '{self.curr_sig_ref}' in {domain} domain!"
                            raise Exception(err_msg)
                        else:
                            # Check if WFC are defined for the signal
                            td = self.patt_exec_block2time_domain[pattern_exec_block]
                            indx = 0
                            for sig in signals:
                                fstn = DomainUtils.get_full_name(td, sig)
                                wfc_list = self.sig2wfc[fstn]
                                wfc = vec_data[indx : indx + 1]
                                if wfc == "%":
                                    if sig in self.proc_sig_wfc_hash:
                                        err_msg = f"Signal '{sig}' can not have both '%' and '#' as WFC!"
                                        raise Exception(err_msg)
                                    elif sig not in self.proc_sig_wfc_percent:
                                        self.proc_sig_wfc_percent.append(sig)
                                    fpn = self.curr_proc_name
                                    if fpn not in self.proc_for_subs:
                                        self.proc_for_subs.append(fpn)
                                elif wfc == "#":
                                    if sig in self.proc_sig_wfc_percent:
                                        err_msg = f"Signal '{sig}' can not have both '%' and '#' as WFC!"
                                        raise Exception(err_msg)
                                    elif sig not in self.proc_sig_wfc_hash:
                                        self.proc_sig_wfc_hash.append(sig)
                                    fpn = self.curr_proc_name
                                    if fpn not in self.proc_for_subs:
                                        self.proc_for_subs.append(fpn)
                                    self.is_found_hash_proc = True
                                elif wfc not in wfc_list:
                                    sig_group_name = DomainUtils.get_name(fsg)
                                    timing_domain = DomainUtils.get_domain(td, True)
                                    err_msg = f"Not defined WFC '{wfc}' for signal {sig} in the signal groups '{sig_group_name}' for the '{timing_domain}' timing domain!"
                                    raise Exception(err_msg)
                                indx += 1
                    else:
                        err_msg = f"Signal or SignalGroup {self.curr_sig_ref} is not defined in Signals group or in SignalGroups {domain} domain!"
                        raise Exception(err_msg)
        self.curr_proc_wfc_order.append(vec_data)

    def b_procedures__pattern_statements__close_vector_block(self, t):
        if self.debug:
            func_name = inspect.stack()[0][3]
            self.trace(func_name, t)
        self.curr_sig_ref = ""

        # Getting condition WFC data before the first vector statement
        if self.is_condition_stmt and self.is_first_vector:
            for pattern_exec_block in self.patt_exec_block2patt_burst.keys():
                patt_bursts = self.patt_exec_block2patt_burst[pattern_exec_block]
                # For every pattern burst block in the pattern exec block
                for patt_burst in patt_bursts:
                    sig_group_domain = self.patt_burst2sig_groups_domain[patt_burst]
                    sig2wfc = WFCUtils.collect_sig2wfc(self.sig2type.keys(),
                                                       sig_group_domain,
                                                       self.signal_groups2signals,
                                                       self.curr_proc_sig_order,
                                                       self.curr_proc_wfc_order)
                    self.proc2first_cond[self.curr_proc_name] = sig2wfc



 

       #Ignore so far the Fixed and Condition statetments        
        if self.is_vector_stmt:
            
            if self.is_first_vector:
                self.is_first_vector = False
                if self.curr_wft == "":
                    err_msg = (
                        "Missing WaveformTable reference before the first vector address!"
                    )
                    raise Exception(err_msg)

        self.curr_sig_ref = ""
        self.curr_proc_sig_order = []
        self.curr_proc_wfc_order = []
        self.curr_proc_cond_wfc_order = []
        self.is_vector_stmt = False
        self.is_condition_stmt = False

    def b_procedures__pattern_statements__KEYWORD_SHIFT(self, t):
        if self.debug:
            func_name = inspect.stack()[0][3]
            self.trace(func_name, t)
        self.proc_with_shift.append(self.curr_proc_name)
        self.pos_rel_shift = HashInfo.POS_SHIFT

    def b_procedures__pattern_statements__close_shift_block(self, t):
        if self.debug:
            func_name = inspect.stack()[0][3]
            self.trace(func_name, t)
        self.pos_rel_shift = HashInfo.POS_AFTER_SHIFT
        self.is_found_hash_proc = False

    def b_procedures__pattern_statements__CALL_VEC_DATA_STRING(self, t):
        if self.debug:
            func_name = inspect.stack()[0][3]
            self.trace(func_name, t)

    def b_procedures__close_proc(self, t):
        if self.debug:
            func_name = inspect.stack()[0][3]
            self.trace(func_name, t)

        proc_name = DomainUtils.get_name(self.curr_proc_name)
        labels = self.proc_labels[self.curr_proc_name]
        gt_labels = self.proc_goto_labels[self.curr_proc_name]
        for label in gt_labels:
            if label not in labels:
                obj = self.proc_goto_label_obj[label]
                err_msg = f"Label {label} used by Goto statament in the Procedure '{proc_name}' is not defined!"
                raise STILSemanticException( obj.line, obj.column, err_msg)

        self.curr_proc_name = ""
        self.pos_rel_shift = HashInfo.POS_UNKNOWN
        self.is_first_vector = True

    def b_procedures__pattern_statements__LOOP_COUNT(self, t):
        if self.debug:
            func_name = inspect.stack()[0][3]
            self.trace(func_name, t)
        if int(t.value) < 1:
            err_msg = "Loop value must be positive!"
            raise Exception(err_msg)
        self.start_loop_va = self.proc2va[self.curr_proc_name]
        self.loop_count = int(t.value)

    def b_procedures__pattern_statements__close_loop_block(self, t):
        if self.debug:
            func_name = inspect.stack()[0][3]
            self.trace(func_name, t)

        # Used to compare test cycles with ATPG patterns files.
        curr_va = self.proc2va[self.curr_proc_name] - 1
        v = (curr_va - self.start_loop_va + 1) * (self.loop_count - 1)
        self.proc2tc[self.curr_proc_name] += v
        self.start_loop_va = 0
        self.loop_count = 0

    def b_procedures__pattern_statements__MATCHLOOP_COUNT(self, t):
        if self.debug:
            func_name = inspect.stack()[0][3]
            self.trace(func_name, t)
        if int(t.value) < 1:
            err_msg = "MatchLoop value must be positive!"
            raise Exception(err_msg)

    def b_procedures__pattern_statements__close_matchloop_block(self, t):
        if self.debug:
            func_name = inspect.stack()[0][3]
            self.trace(func_name, t)

    def b_procedures__close_procedure_block(self, t):
        if self.debug:
            func_name = inspect.stack()[0][3]
            self.trace(func_name, t)
            for key in self.proc_domain2proc_names.keys():
                proc_names = self.proc_domain2proc_names.get(key)
                for name in proc_names:
                    print(f" procedure domain {key} -> procedure name {name}")
        self.curr_proc_domain = DomainUtils.global_domain
