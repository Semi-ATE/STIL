# -*- coding: utf-8 -*-

class SigTimingInfo:

    def __init__(self, signal):
        self.signal = signal
        # key is wfc, value is list of tuples (wfe + time offset)
        self.wfc2wfe_time = {}

    def replace_timing_for_wfc(self, wfc, wfe, old_time, new_time):
                
        if wfc in self.wfc2wfe_time:
            pairs = self.wfc2wfe_time[wfc]
            old_value = (wfe, old_time)
            i = pairs.index(old_value) 
            pairs[i] = (wfe, new_time)
        
    def set_timing_for_wfc(self, wfc, wfe, time):

        if wfc in self.wfc2wfe_time:
            pairs = self.wfc2wfe_time[wfc]
            value = (wfe, time)
            pairs.append(value)
        else:
            self.wfc2wfe_time[wfc] = [(wfe, time)]

    def get_wfcs(self):
        '''
        Returns all available WFC for current signal

        Returns
        -------
        List of WFC.

        '''
        return self.wfc2wfe_time.keys()
    
    def get_timing_for_wfc(self, wfc):
        '''
        Returns list of WFE and Timing pair for the given WFC

        Returns
        -------
        List of WFE+Timing.

        '''
        if wfc in self.wfc2wfe_time:
            return self.wfc2wfe_time[wfc]
        else:
            return None
        
    def __str__(self):
        data = f"signal {self.signal} "
        for wfc in self.wfc2wfe_time:
            data += "\nWFC " + wfc + " => " 
            pairs = self.wfc2wfe_time[wfc]
            for p in pairs:
                data += str(p[1]) + ":" + str(p[0]) + " | " 
        return data