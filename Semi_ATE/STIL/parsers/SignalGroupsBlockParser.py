# -*- coding: utf-8 -*-
import inspect

from .DomainUtils import DomainUtils

class SignalGroupsBlockParser:
    def __init__(self, debug=False):
        self.debug = debug
        # List with all parsed signal groups domains
        self.signal_groups_domains = []
        # dict key   is the signal group name with the domain -> domain::signal_group
        # dict value is a list with all signals defined for the key signal group
        self.signal_groups2signals = {}

        # Current full signal group name (domain::signal_group)
        self.curr_sig_group_name = None
        # Current domain name
        self.curr_sig_group_domain = DomainUtils.global_domain
        self.last_op = None
        # All signal groups names without domain
        # Will be used in Macro/Proc blocks validation
        self.all_signal_groups = []

        self.is_signalgroups_block_defined = False
        
        # dict key   is the signal_groups_domain::signal name
        # dict value is the default drive state of the signal if not used
        self.sgd_sig2def_state = {}


    def trace(self, func_name, t):
        head = f"{__name__}:{func_name}"

        if isinstance(t, list):
            print(f"{head} rule value {t}")
        else:
            print(f'{head} token value "{t}" at line {t.line} column {t.column}')

    def b_signal_groups__SIGNAL_GROUPS_DOMAIN_NAME(self, t):
        if self.debug:
            func_name = inspect.stack()[0][3]
            self.trace(func_name, t)
        self.curr_sig_group_domain = t.value

    def b_signal_groups__open_signal_groups_block(self, t):
        if self.debug:
            func_name = inspect.stack()[0][3]
            self.trace(func_name, t)
        if self.is_signal_block_defined == False:
            err_msg = "Expected Signal block before any SignalGroups block"
            raise Exception(err_msg)
        self.is_signalgroups_block_defined = True

        if self.curr_sig_group_domain in self.signal_groups_domains:
            domain_name = DomainUtils.get_domain(self.curr_sig_group_domain, True)
            err_msg = f"SignalGroups block domain '{domain_name}' is already defined"
            raise Exception(err_msg)
        else:
            self.signal_groups_domains.append(self.curr_sig_group_domain)

    def b_signal_groups__SIGNAL_GROUP_NAME(self, t):
        if self.debug:
            func_name = inspect.stack()[0][3]
            self.trace(func_name, t)
        sig_group_name = t.value
        if sig_group_name in self.sig2type:
            err_msg = f"Signal group name '{sig_group_name}' is already defined as signal in the Signals block"
            raise Exception(err_msg)
        self.curr_sig_group_name = DomainUtils.get_full_name(
            self.curr_sig_group_domain, t.value
        )

        if self.curr_sig_group_name in self.signal_groups2signals:
            err_msg = f"Signal group name '{sig_group_name}' is already defined"
            raise Exception(err_msg)
        else:
            self.signal_groups2signals[self.curr_sig_group_name] = []

        if sig_group_name not in self.all_signal_groups:
            self.all_signal_groups.append(sig_group_name)
            
            

    def b_signal_groups__SIG_ADD(self, t):
        if self.debug:
            func_name = inspect.stack()[0][3]
            self.trace(func_name, t)
        self.last_op = t.value

    def b_signal_groups__SIG_SUB(self, t):
        if self.debug:
            func_name = inspect.stack()[0][3]
            self.trace(func_name, t)
        self.last_op = t.value

    def b_signal_groups__SIGREF_NAME(self, t):
        if self.debug:
            func_name = inspect.stack()[0][3]
            self.trace(func_name, t)
        sig_name = t.value
        sig_list = self.signal_groups2signals[self.curr_sig_group_name]
        sig_group = DomainUtils.get_full_name(self.curr_sig_group_domain, sig_name)

        if sig_name in self.sig2type:
            # if the sigref is a signal
            if self.last_op == None:
                sig_list.append(sig_name)
            elif self.last_op == "+":
                if sig_name in sig_list:
                    name = DomainUtils.get_name(self.curr_sig_group_name)
                    err_msg = f"In the signal group '{name}', can not add already existing signal '{sig_name}' from previously used signal groups or signal in the current signals group"
                    raise Exception(err_msg)
                else:
                    sig_list.append(sig_name)
            elif self.last_op == "-":
                if sig_name not in sig_list:
                    name = DomainUtils.get_name(self.curr_sig_group_name)
                    err_msg = f"In the signal group '{name}', can not remove not existing signal '{sig_name}' from previously used signal groups or signal in the current signals group"
                    raise Exception(err_msg)
                else:
                    sig_list.remove(sig_name)
            else:
                err_msg = "Internal error, expecting '+' or '-' operator"
                raise Exception(err_msg)

        elif sig_group in self.signal_groups2signals:
            # if the sigref is a signal group
            signals = self.signal_groups2signals[sig_group]
            if self.last_op == None:
                sig_list.extend(signals)
            elif self.last_op == "+":
                check = any(item in sig_list for item in signals)
                if check:
                    name = DomainUtils.get_name(self.curr_sig_group_name)
                    err_msg = f"Can not add signal group '{sig_name}' into signal group '{name}' because at least one signal is duplicated in both groups"
                    raise Exception(err_msg)
                else:
                    sig_list.extend(signals)
            elif self.last_op == "-":
                check = all(item in sig_list for item in signals)
                if check:
                    for s in signals:
                        sig_list.remove(s)
                else:
                    name = DomainUtils.get_name(self.curr_sig_group_name)
                    err_msg = f"Can not remove signal group '{sig_name}' from signal group '{name}' because not all signals from '{sig_name}' exists in previously used signal groups"
                    raise Exception(err_msg)
        else:
            # raise an error, because the sigref is not defined
            err_msg = f"Signal {sig_name} is not defined in the Signals block"
            raise Exception(err_msg)
        self.last_op = None

    def b_signal_groups__SIG_DEF_STATE_UP(self, t):
        if self.debug:
            func_name = inspect.stack()[0][3]
            self.trace(func_name, t)

        self.sig2def_state[self.curr_sig_group_name] = "U"

    def b_signal_groups__SIG_DEF_STATE_DOWN(self, t):
        if self.debug:
            func_name = inspect.stack()[0][3]
            self.trace(func_name, t)

        self.sig2def_state[self.curr_sig_group_name] = "D"

    def b_signal_groups__SIG_DEF_STATE_OFF(self, t):
        if self.debug:
            func_name = inspect.stack()[0][3]
            self.trace(func_name, t)

        self.sig2def_state[self.curr_sig_group_name] = "Z"
        
    def b_signal_groups__SIGNAL_LIST_END_STMT(self, t):
        if self.debug:
            func_name = inspect.stack()[0][3]
            self.trace(func_name, t)
        sigs = self.signal_groups2signals[self.curr_sig_group_name]
        if len(sigs) == 0:
            sig_group = DomainUtils.get_name(self.curr_sig_group_name)
            err_msg = f"Signal group {sig_group} does not have signals"
            raise Exception(err_msg)
        self.curr_sig_group_name = None

    def b_signal_groups__close_signal_attr_block(self, t):
        if self.debug:
            func_name = inspect.stack()[0][3]
            self.trace(func_name, t)
        self.curr_sig_group_name = None

    def b_signal_groups__close_signal_groups_block(self, t):
        if self.debug:
            func_name = inspect.stack()[0][3]
            self.trace(func_name, t)
        self.curr_sig_group_domain = DomainUtils.global_domain
