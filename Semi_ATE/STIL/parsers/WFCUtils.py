# -*- coding: utf-8 -*-
import re

from .DomainUtils import DomainUtils


class WFCUtils:

    debug = False

    def __init__(self):
        pass

    def trim_wfcs(wfc_list):
        if WFCUtils.debug:
            print("WFCUtils::trim_wfcs")
        return re.sub(r"\s+", "", wfc_list)

    def expand_wfcs(wfc_list):
        """
        This function will expand WFC sequence in single continious string
        Useful in the case when macro/procedure are called with signal's WFC

        LH 0 1         -> LH01
        LH \r2 01 XX X -> LH0101XXX
        """
        if WFCUtils.debug:
            print("WFCUtils::expand_wfcs")

        wfcs = ""
        
        # Check if the WFCs list contain "\j" join command
        join_pos = wfc_list.find("\\j")
        if join_pos != -1:
            wfc_list = wfc_list[join_pos+2:]

        # Check if the WFCs list contain "\m" map command
        map_pos = wfc_list.find("\\m")
        if map_pos != -1:
            wfc_list = wfc_list[map_pos+2:]

        # Check if the WFCs list contain "\r" repeat command
        repeat_pos = wfc_list.find("\\r")
        if repeat_pos == -1:
            # no repeat commans, just remove all white spaces
            wfcs = re.sub(r"\s+", "", wfc_list)
        else:
            start_pos = 0
            # collect all WFC before the first /r command
            wfcs += wfc_list[start_pos:repeat_pos]
            while start_pos != -1:

                if repeat_pos == -1:
                    # the last segment
                    repeat_list = wfc_list[start_pos:]
                else:
                    # get one segment with /r command
                    repeat_list = wfc_list[start_pos:repeat_pos]
                # split by empty space to colect the repeat value /rXXX
                parts = repeat_list.split(" ")

                repeat_value = parts[0][2:]
                if len(repeat_value) > 0:
                    r = int(repeat_value.strip(), base=10)
                    for i in range(r):
                        # repeat the WFCs "r" times
                        wfcs += parts[1]
                elif parts[0].startswith("\\r"):
                    raise Exception("Missing repeat value after \\r command")
                # Adding rest of the WFCs after repeat statement
                if len(parts) > 2:
                    for i in range(len(parts) - 2):
                        wfcs += parts[i + 2]
                if repeat_pos == -1:
                    start_pos = -1
                else:
                    # search for the next repeat command
                    start_pos = repeat_pos
                    repeat_pos = wfc_list.find("\\r", repeat_pos + 1)
            wfcs = re.sub(r"\s+", "", wfcs)

        return wfcs

    def collect_sig2wfc(signals, 
                        sig_group_domain,
                        signals_group2signals,
                        curr_signals,
                        curr_wfcs,
                        last_sig2wfc = None,
                        sig2wfc_before_subs = None
                        ):
        """
        This function will collect WFC for every signal in a vector or condition
        statement. If last_sig2wfc is given, it will fill missing sig2wfc
        Will return a dict with signal name as key and WFC as value.
        signals -> list with signal names
        sig_group_domain -> signals group domain name
        signals_group2signals -> dict with key domain::signals_group and key list of signals names
        curr_signals -> list with signals or signals groups
        curr_wfcs -> list with single (per signal) or multiple (per signals group) WFC
        last_sig2wfc -> last known state of signals and their WFC (optional). 
                        Key is the signal name, value is a WFC
        sig2wfc_before_subs -> last known WFC for signals before first # or %
        """        
        if WFCUtils.debug:
            print("WFCUtils::collect_sig2wfc")
            print(f"WFCUtils::collect_sig2wfc signals {signals}")
            print(f"WFCUtils::collect_sig2wfc sig_group_domain {sig_group_domain}")
            print(f"WFCUtils::collect_sig2wfc signals_group2signals {signals_group2signals}")
            print(f"WFCUtils::collect_sig2wfc curr_signals {curr_signals}")
            print(f"WFCUtils::collect_sig2wfc curr_wfcs {curr_wfcs}")
            print(f"WFCUtils::collect_sig2wfc last_sig2wfc {last_sig2wfc}")
            print(f"WFCUtils::collect_sig2wfc sig2wfc_before_subs {sig2wfc_before_subs}")

        sig2wfc = {}
        found_sigs = []
        sig_indx = 0
        for sig in curr_signals:

            sg = DomainUtils.get_full_name(sig_group_domain, sig)

            if sig in signals:
                wfc = curr_wfcs[sig_indx]
                sig2wfc[sig] = [wfc]
                sig_indx += 1
                found_sigs.append(sig)
                
                if wfc == '#' or wfc == '%':
                    if sig not in sig2wfc_before_subs:
                        last_wfc = last_sig2wfc[sig][0]
                        sig2wfc_before_subs[sig] = last_wfc

                if WFCUtils.debug:
                    print(f"WFCUtils::collect_sig2wfc signal {sig} wfc {wfc}")

            elif sg in signals_group2signals:
                si = 0
                for sigg in signals_group2signals[sg]:
                    wfc = curr_wfcs[sig_indx]
                    #print(f" wfc {wfc} for sig index {sig_indx} signal {sigg}")
                    sig2wfc[sigg] = [wfc[si]]
                    found_sigs.append(sigg)
                    si += 1

                    """
                    In the standard is not specified exactly which WFC should 
                    be used in delta vector after WFC substitution like:
                        
                    V {sig = WFC}// Last defined WFC before WFC substitution
                    V {sig = #}  // WFC substitution
                    V {}         // Delta vector, which WFC should be placed here?
                    
                    The implementation will set in the delta vector, the last 
                    defined WFC before the first substituted WFC (# or %). 
                    This is based 
                    
                    """
                    if wfc == '#' or wfc == '%':
                        last_wfc = last_sig2wfc[sigg][0]
                        sig2wfc_before_subs[sigg] = last_wfc

                    if WFCUtils.debug:
                        print(f"WFCUtils::collect_sig2wfc signal {sigg} wfc {sig2wfc[sigg]}")
                sig_indx += 1
            else:
                raise Exception(f"Error can not find signal/signal group named {sig}")
        
        # Fill with missing wfc and signals
        if last_sig2wfc != None:
            for sig in last_sig2wfc:
                if sig not in found_sigs:
                    last_wfc = last_sig2wfc[sig][0]
                    if last_wfc == "#" or last_wfc == "%":
                        if sig2wfc_before_subs == None:
                            err = f"For signal {sig}, there is no defined WFC before first '#' or '%'"
                            raise Exception(err)
                        else:
                            if sig in sig2wfc_before_subs:
                                sig2wfc[sig] = [sig2wfc_before_subs[sig]]
                            else:
                                # Issue #13
                                # At this time is unknown which WFC should be placed
                                # When Macro/Proc call arguments are known, the '?' 
                                # should be replaced with the last used WFC in '#'
                                sig2wfc[sig] = '?'
                    else:
                        sig2wfc[sig] = [last_sig2wfc[sig][0]]
                
        return sig2wfc

    def collect_va_wfcs(
        signal_groups_domains,
        pattern,
        patt2sig_order,
        curr_sig_order,
        curr_wfc_order,
        last_wfc_order,
        signals,
        signal_groups2signals,
    ):
        """
        This function will collect WFC sequence for a vector address,
        based on signal order and WFC sequence from the last vector.

        V {sig1 = 0; sig2 = L; sig3 = X;} // VA=0 -> 0LX
        V {sig3 = H;}                     // VA=1 -> 0LH
        The VA=1 does not contain all required WFC, so according
        STIL Standard, the latest defined WFC (at VA=0) will be used.

        curr_sig_order -> list with signal/SignalsGroup for the current VA
        curr_wfc_order -> list with WFC for the current VA
        last_wfc_order -> WFCs in the last VA
        signal_order   -> list with signal order in the first VA of the pattern block

        """
        if WFCUtils.debug == False:
            print("WFCUtils::collect_va_wfcs")
            print(f"WFCUtils::collect_va_wfcs curr_sig_order {curr_sig_order}")
            print(f"WFCUtils::collect_va_wfcs curr_wfc_order {curr_wfc_order}")
            print(f"WFCUtils::collect_va_wfcs last_wfc_order {last_wfc_order}")

        wfcs = ""

        for sp in signal_groups_domains:
            key = DomainUtils.get_full_name(sp, pattern)
            print(f"key {key}")
            if key in patt2sig_order:
                sig_order = patt2sig_order[key]
                print(f"sig_order {sig_order} for {key}")

                si = 0
                for sig_o in sig_order:
                    print(f"Process signal {sig_o}")
                    for sigs in curr_sig_order:
                        print(f"\t compare to {sigs}")
                        if sigs == sig_o:
                            i = curr_sig_order.index(sigs)
                            wfc = curr_wfc_order[i]
                            print(f"s signal {sigs} wfc {wfc}")
                            wfcs += wfc
                            break
                        else:
                            for sgd in signal_groups_domains:
                                key = DomainUtils.get_full_name(sgd, sigs)
                                if key in signal_groups2signals:
                                    signals = signal_groups2signals[key]
                                    for sig in signals:
                                        if sig == sig_o:
                                            wfc = curr_wfc_order[0][si]
                                            wfcs += wfc
                                            print(f"sg signal {sig} wfc {wfc}")
                                            si += 1
                                            break

        if WFCUtils.debug == False:
            print(f"WFCUtils::collect_va_wfcs return value {wfcs}")

        return wfcs

    def find_hash(wfc_list):
        """
        This function will return position of all # in a list of WFCs

        """
        plist = []
        pos = wfc_list.find("#")
        while pos != -1:
            plist.append(pos)
            pos = wfc_list.find("#", pos + 1)
        return plist
