# -*- coding: utf-8 -*-


class HashInfo:

    POS_UNKNOWN = -1
    POS_BEFORE_SHIFT = 0
    POS_SHIFT = 1
    POS_AFTER_SHIFT = 2

    def __init__(self, pos_rel_shift, sig_ref, pos, debug=False):
        # Position relative to the shift
        self.pos_rel_shift = pos_rel_shift
        # Signal reference
        self.sig_ref = sig_ref
        # list of position of the # inside WFC list of the signal reference
        # [2, 5] if you have the following WFC list : 00#LX#X
        self.pos = pos
    
    def __str__(self):

        pos = "in unknwown position"
        if self.pos_rel_shift == HashInfo.POS_BEFORE_SHIFT:
            pos = "before the Shift block"
        elif self.pos_rel_shift == HashInfo.POS_AFTER_SHIFT:
            pos = "after the Shift block"
        elif self.pos_rel_shift == HashInfo.POS_SHIFT:
            pos = "in the Shift block"
            
        s = f"# at pos {self.pos} for signal/signal group {self.sig_ref} "+pos
        return s