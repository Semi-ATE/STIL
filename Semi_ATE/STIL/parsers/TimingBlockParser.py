# -*- coding: utf-8 -*-
import inspect

from .DomainUtils import DomainUtils
from .WFCUtils import WFCUtils
from .SigTimingInfo import SigTimingInfo


class TimingBlockParser:

    force_events = [
        "ForceDown",
        "D",
        "ForceUp",
        "U",
        "ForceOff",
        "Z",
        "ForcePrior",
        "P",
    ]
    compare_events = [
        "CompareLow",
        "L",
        "CompareHigh",
        "H",
        "CompareUnknown",
        "X",
        "x",
        "CompareOff",
        "T",
        "CompareValid",
        "V",
        "CompareLowWindow",
        "l",
        "CompareOff",
        "h",
        "CompareHighWindow",
        "h",
        "CompareOffWindow",
        "t",
        "CompareValidWindow",
        "v",
        
    ]

    def __init__(self, debug=False):
        self.debug = debug
        # List with all parsed timing domains
        self.timing_domains = []

        self.curr_signal_groups_domain = DomainUtils.global_domain
        self.curr_timing_domain = DomainUtils.global_domain

        # signal expression references in Timing block
        # can be either single signal or group of signals
        self.curr_sigref = []

        # dict key   is the signal in full domain name : timing_domain::signal_name
        # dict value is a list with all WFC defined for this signal/domain
        self.sig2wfc = {}

        # dict key   is the timing_domain::wft::signal_name
        # dict value is a SigTimingInfo object with timing information 
        self.sig_wft2timing = {}

        # dict key   is the timing domain name
        # dict value is a list with all waveform tables (WFT)
        self.time_domain2wft = {}

        self.curr_wft = ""

        self.curr_wfc_list = ""

        self.curr_wfe_count = 0

        self.curr_sig_type = ""

        self.curr_events = []

        # dict key   is the timing_domain::wft
        # dict value is the wft's period value.
        self.wft2period = {}

        self.is_timing_block_defined = False

    def trace(self, func_name, t):
        head = f"{__name__}:{func_name}"

        if isinstance(t, list):
            print(f"{head} rule value {t}")
        else:
            print(f'{head} token value "{t}" at line {t.line} column {t.column}')

    def b_timing__TIMING_DOMAIN_NAME(self, t):
        if self.debug:
            func_name = inspect.stack()[0][3]
            self.trace(func_name, t)
        self.curr_timing_domain = t.value

    def b_timing__open_timing_block(self, t):
        if self.debug:
            func_name = inspect.stack()[0][3]
            self.trace(func_name, t)

        if self.is_signal_block_defined == False:
            err_msg = "Expected Signal block before any Timing block"
            raise Exception(err_msg)
        if self.is_signalgroups_block_defined == False:
            err_msg = "Expected SignalGroups block before any Timing block"
            raise Exception(err_msg)
        self.is_timing_block_defined = True

        if self.curr_timing_domain in self.timing_domains:
            domain_name = DomainUtils.get_domain(self.curr_timing_domain, True)
            err_msg = f"Timing block domain '{domain_name}' is already defined !"
            raise Exception(err_msg)
        else:
            self.timing_domains.append(self.curr_timing_domain)

    def b_timing__WFT_NAME(self, t):
        if self.debug:
            func_name = inspect.stack()[0][3]
            self.trace(func_name, t)
        self.curr_wft = t.value

        if self.curr_timing_domain in self.time_domain2wft:
            wft_list = self.time_domain2wft[self.curr_timing_domain]
            if self.curr_wft in wft_list:
                err_msg = f"Waveform Table named '{self.curr_wft}' is already defined"
                raise Exception(err_msg)
            else:
                wft_list.append(self.curr_wft)
        else:
            self.time_domain2wft[self.curr_timing_domain] = [self.curr_wft]

    def b_timing__period(self, t):
        if self.debug:
            func_name = inspect.stack()[0][3]
            self.trace(func_name, t)
            
        key = self.curr_timing_domain + "::" + self.curr_wft
        self.wft2period[key] = t[1].value
        
    def b_timing__SIGNAL_GROUPS_DOMAIN(self, t):
        if self.debug:
            func_name = inspect.stack()[0][3]
            self.trace(func_name, t)
        sig_groups = t.value
        if sig_groups not in self.signal_groups_domains:
            err_msg = f"Signal groups domain {sig_groups} is not defined"
            raise Exception(err_msg)
        self.curr_signal_groups_domain = t.value

    def b_timing__WF_SIGREF_EXPR(self, t):
        if self.debug:
            func_name = inspect.stack()[0][3]
            self.trace(func_name, t)

        sig_ref = t.value

        if sig_ref in self.sig2type:
            self.curr_sig_type = self.sig2type[sig_ref]
            ftn = DomainUtils.get_full_name(self.curr_timing_domain, sig_ref)
            self.curr_sigref.append(ftn)
        else:
            sig_group_domain = self.curr_signal_groups_domain
            fsn = DomainUtils.get_full_name(sig_group_domain, sig_ref)
            if fsn in self.signal_groups2signals:
                signals = self.signal_groups2signals[fsn]
                sig_type = ""
                for signal in signals:

                    if sig_type != "":
                        new_sig_type = self.sig2type[signal]
                        if sig_type == "In" and new_sig_type == "Out":
                            err_msg = "Signal '{sig_ref}' contain both input and output signals, which can not be used for defining WaveForm Characters!"
                            raise Exception(err_msg)
                        elif sig_type == "Out" and new_sig_type == "In":
                            err_msg = "Signal '{sig_ref}' contain both input and output signals, which can not be used for defining WaveForm Characters!"
                            raise Exception(err_msg)
                        pass
                    else:
                        st = self.sig2type[signal]
                        if st == "In" or st == "Out":
                            sig_type = st

                    ftn = DomainUtils.get_full_name(self.curr_timing_domain, signal)
                    self.curr_sigref.append(ftn)
            else:
                domain = DomainUtils.get_domain(sig_group_domain, True)
                err_msg = f"Signal {sig_ref} from '{domain}' domain is not defined"
                raise Exception(err_msg)

    def check_if_wfc_defined(self, sigref, wfc):

        sig = DomainUtils.get_name(sigref)
        full_sig_name = self.curr_timing_domain + '::' + self.curr_wft + '::' + sig
        
        if full_sig_name in self.sig_wft2timing:
            sig_time_info = self.sig_wft2timing[full_sig_name]
            if sig_time_info is not None:
                timing = sig_time_info.get_timing_for_wfc(wfc)
                if timing is not None:
                    err_msg = f"WFC {wfc} is already defined for signal {sig}"
                    raise Exception(err_msg)
            

    def b_timing__WFC_LIST(self, t):
        if self.debug:
            func_name = inspect.stack()[0][3]
            self.trace(func_name, t)

        self.curr_wfc_list = t.value

        for sigref in self.curr_sigref:
            wfcs = WFCUtils.trim_wfcs(self.curr_wfc_list)
            if sigref in self.sig2wfc:
                for wfc in wfcs:

                    self.check_if_wfc_defined(sigref, wfc)
                    
                    stored_wfc = self.sig2wfc[sigref]
                    if wfc not in stored_wfc:
                        self.sig2wfc[sigref] += wfc
            else:
                self.sig2wfc[sigref] = wfcs

    def b_timing__EVENT(self, t):
        if self.debug:
            func_name = inspect.stack()[0][3]
            self.trace(func_name, t)
            
        wfe = t.value

        if wfe != "/":
            self.curr_wfe_count += 1
            if self.curr_sig_type == "In":
                if wfe not in TimingBlockParser.force_events:
                    err_msg = f"Compare Waveform event '{wfe}' is used for 'In' type of signal !"
                    raise Exception(err_msg)
            elif self.curr_sig_type == "Out":
                if wfe not in TimingBlockParser.compare_events:
                    err_msg = f"Force Waveform event '{wfe}' is used for 'Out' type of signal !"
                    raise Exception(err_msg)
        self.curr_events.append(wfe)

    def b_timing__time_offset(self, t):
        if self.debug:
            func_name = inspect.stack()[0][3]
            self.trace(func_name, t)

        wfe_count = self.curr_wfe_count
        wfc_count = len(self.curr_wfc_list)
        if wfe_count > 1 and wfe_count != wfc_count:
            err_msg = f"Number of Waveform Events ({wfe_count}) does not match with number of Waveform Chars ({wfc_count})"
            raise Exception(err_msg)
            
        for domain_sig in self.curr_sigref:
            
            sig = DomainUtils.get_name(domain_sig)
            
            full_sig_name = self.curr_timing_domain + '::' + self.curr_wft + '::' + sig
            
            if full_sig_name not in self.sig_wft2timing:
                sig_time_info = SigTimingInfo(sig)
                self.sig_wft2timing[full_sig_name] = sig_time_info
            else:
                sig_time_info = self.sig_wft2timing[full_sig_name]
            
            index = 0
            for wfc in self.curr_wfc_list:
                if len(self.curr_events) == 1:
                    sig_time_info.set_timing_for_wfc(wfc, self.curr_events[0], t[0] )
                else:
                    sig_time_info.set_timing_for_wfc(wfc, self.curr_events[index], t[0] )
                index += 1
            

        self.curr_events.clear()
        self.curr_wfe_count = 0
        self.curr_sig_type = ""

    def b_timing__close_wfc_block(self, t):
        if self.debug:
            func_name = inspect.stack()[0][3]
            self.trace(func_name, t)
            
        self.curr_sigref.clear()
        self.curr_wfc_list = ""
        self.curr_events.clear()

    def b_timing__close_timing_block(self, t):
        if self.debug:
            func_name = inspect.stack()[0][3]
            self.trace(func_name, t)
        self.curr_timing_domain = DomainUtils.global_domain
        self.curr_wft = ""
